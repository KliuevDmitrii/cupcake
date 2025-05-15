import allure
from time import sleep
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

class SearchPage:
    """
    Этот класс предоставляет методы для выполнения действий на странице поиска.
    """

    def __init__(self, driver: WebDriver) -> None:
        url = ConfigProvider().get("ui", "search_url")
        self.__url = url
        self.__driver = driver

    @allure.step("Перейти на страницу поиска")
    def go(self):
        self.__driver.get(self.__url)
        self.__driver.refresh()

        try:
            WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//textarea[@id="sb_form_q"]'))
            )
        except TimeoutException:
            try:
                WebDriverWait(self.__driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="ybar-sbq"]'))
                )
            except TimeoutException:
                screenshot = self.__driver.get_screenshot_as_png()
                allure.attach(screenshot, name="search_input_not_found", attachment_type=allure.attachment_type.PNG)
                pytest.fail("Не удалось найти поле ввода поиска ни по первому, ни по второму локатору")

    @allure.step("Ввести наименование мерчанта и нажать поиск в поисковике")
    def enter_merch_name(self, merch_name: str):
        search_input = self.__get_search_input_element()
        search_input.clear()
        search_input.send_keys(merch_name)
        sleep(3)
        search_input.send_keys(Keys.ENTER)

    def clear_search_field(self):
        search_input = self.__get_search_input_element()
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(Keys.DELETE)

    def __get_search_input_element(self):
        wait = WebDriverWait(self.__driver, 10)
        try:
            return wait.until(
                EC.presence_of_element_located((By.XPATH, '//textarea[@id="sb_form_q"]'))
            )
        except TimeoutException:
            try:
                return wait.until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="ybar-sbq"]'))
                )
            except TimeoutException:
                screenshot = self.__driver.get_screenshot_as_png()
                allure.attach(screenshot, name="search_input_not_found", attachment_type=allure.attachment_type.PNG)
                pytest.fail("Не удалось найти поле поиска по ни одному из ожидаемых локаторов.")

    @allure.step("Ждём появление серпа")
    def wait_for_serp(self):
        sleep(5)
        wait = WebDriverWait(self.__driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "shadow-root-monetha")]')))

    @allure.step("Проверить наличие серпа и правильность процента кэшбэка")
    def verify_serp_cashback(self, expected_cashback: str):
        wait = WebDriverWait(self.__driver, 15)
        
        try:
            shadow_host = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "shadow-root-monetha")]'))
            )
            assert shadow_host is not None, "Не найден shadow host для кэшбэка"

            shadow_root = shadow_host.shadow_root
            
            cashback_element = shadow_root.find_element(
                By.CSS_SELECTOR,
                '#monetha-sr span span'
            )
            actual_cashback = cashback_element.text.strip()

            print(f"Найденный процент кэшбэка: {actual_cashback}")

            actual_value = round(float(actual_cashback.replace("%", "").replace(",", ".").strip()), 1)
            expected_value = round(float(expected_cashback.replace("%", "").replace(",", ".").strip()), 1)
            
            actual_cashback_formatted = f"{actual_value}%"
            expected_cashback_formatted = f"{expected_value}%"

            assert expected_cashback_formatted == actual_cashback_formatted, (
                f"Ожидался процент кэшбэка '{expected_cashback_formatted}', но найдено '{actual_cashback_formatted}'"
            )
            
        except Exception as e:
            assert False, f"Не удалось найти элемент с кэшбэком или ошибка при доступе к shadow DOM: {str(e)}"
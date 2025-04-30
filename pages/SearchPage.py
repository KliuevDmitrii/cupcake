import allure
from time import sleep
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
        WebDriverWait(self.__driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//textarea[@id="sb_form_q"]'))
    )

    @allure.step("Ввести наименование мерчанта и нажать поиск")
    def enter_merch_name(self, merch_name: str):
        wait = WebDriverWait(self.__driver, 15)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@id="sb_form_q"]')))
        element.send_keys(merch_name)
        sleep(2)
        element.send_keys(Keys.ENTER)

    def clear_search_field(self):
        search_input = self.__get_search_input_element()
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(Keys.DELETE)

    def __get_search_input_element(self):
        return self.__driver.find_element(By.XPATH, '//textarea[@id="sb_form_q"]')

    @allure.step("Ждём появление серпа")
    def wait_for_serp(self):
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
            
            cashback_element = shadow_root.find_element(By.CSS_SELECTOR, "span.ex-qn03r")
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
import allure
import pytest
import traceback
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from configuration.ConfigProvider import ConfigProvider

class ExtensionPage:
    """
    Этот класс предоставляет методы для выполнения действий в расширении.
    """
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        self.wait = WebDriverWait(driver, 20)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.__driver.current_url

    @allure.step("Ожидание появления попапа расширения")
    def wait_for_popup(self):
        wait = WebDriverWait(self.__driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "shadow-root-monetha")]')))

    def get_shadow_root(self):
        shadow_host = self.__driver.find_element(By.CSS_SELECTOR, "div.shadow-root-monetha")
        return shadow_host.shadow_root

    @allure.step("Нажать кнопку активации в popup на странице мерчанта")
    def click_activate_button(self):
        shadow = self.get_shadow_root()
        button = shadow.find_element(By.CSS_SELECTOR, "button.ex-tgjvs.ex-zrp4o.ex-wa6h7.ex-tbr8v.ex-wxnf0.ex-ahmr2")
        button.click()

    @allure.step("Ожидание отображения правильного процента кэшбэка")
    def wait_for_cashback_text(self, expected_cashback: str, timeout: int = 25):
        shadow = self.get_shadow_root()

        def cashback_matches(driver):
            try:
                elements = shadow.find_element(
                By.CSS_SELECTOR,
                'div[id="monetha-sr"] div span'
                )
                for el in elements:
                    text = el.text.strip()
                    if expected_cashback in text:
                        print(f"[DEBUG] Найден ожидаемый кэшбэк: {text}")
                        return True
                    elif "%" in text:
                        print(f"[DEBUG] Другой кэшбэк в процессе: {text}")
            except Exception as e:
                print(f"[DEBUG] Ошибка при поиске кэшбэка: {e}")
            return False

        WebDriverWait(self.__driver, timeout).until(cashback_matches)

    @allure.step("Получить текст с кэшбэком из попапа")
    def get_cashback_text(self) -> str:
        shadow = self.get_shadow_root()
        elements = shadow.find_element(
        By.CSS_SELECTOR,
        'div[id="monetha-sr"] div span'
        )
        for el in elements:
            if "%" in el.text:
                return el.text.strip()
        return ""
    
    @allure.step("Проверить наличие popup и правильность процента кэшбэка")
    def verify_popup_cashback(self, expected_cashback: str, timeout: int = 25):
        wait = WebDriverWait(self.__driver, timeout)

        try:
            shadow_host = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.shadow-root-monetha"))
            )
            assert shadow_host is not None, "Не найден shadow host попапа"

            shadow_root = shadow_host.shadow_root

            cashback_element = shadow_root.find_element(
            By.CSS_SELECTOR,
            'div[id="monetha-sr"] div span'
            )
            actual_cashback = cashback_element.text.strip()

            print(f"[DEBUG] Найден кэшбэк в попапе: {actual_cashback}")

            actual_value = round(float(actual_cashback.replace("%", "").replace(",", ".").strip()), 1)
            expected_value = round(float(expected_cashback.replace("%", "").replace(",", ".").strip()), 1)

            actual_cashback_formatted = f"{actual_value}%"
            expected_cashback_formatted = f"{expected_value}%"

            assert actual_cashback_formatted == expected_cashback_formatted, (
                f"Ожидался кэшбэк '{expected_cashback_formatted}', но найден '{actual_cashback_formatted}'"
            )

        except Exception as e:
            assert False, f"Ошибка при проверке кэшбэка в попапе: {str(e)}"

    
    @allure.step("Проверка popup активированного кэшбэка на странице мерчанта")
    def is_cashback_activated(self) -> bool:
        return self.get_status_text().lower() in ["activated", "активировано"]

    @allure.step("Возвращаем текст статуса кэшбэка, например 'Activated'")
    def get_status_text(self, timeout: int = 15) -> str:
        try:
            status_element = WebDriverWait(self.__driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.ex-tllw9.ex-ul0w1"))
            )
            return status_element.text.strip()
        except Exception as e:
            raise Exception(f"Не удалось получить текст статуса из попапа: {str(e)}")

    @allure.step('Проверка наличия текста "Come here often?" в попапе')
    def check_popup_header(self):
        sleep(3)
        shadow_root = self.get_shadow_root()
        header = shadow_root.find_element(By.CSS_SELECTOR, "h3")
        assert "Come here often?" in header.text, "Заголовок попапа не соответствует ожидаемому"

    @allure.step('Проверка наличия текста "" в попапе после нажатия на кнопку ""')
    def check_popup_header_ready(self):
        sleep(3)
        shadow_root = self.get_shadow_root()
        header = shadow_root.find_element(By.CSS_SELECTOR, "h3")
        assert "Come here often?" in header.text, "Заголовок попапа не соответствует ожидаемому"
import allure
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

class ExtensionPage:
    """
    Этот класс предоставляет методы для выполнения действий в расширении.
    """
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        self.wait = WebDriverWait(driver, 20)

    def wait_for_popup(self):
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.shadow-root-monetha"))
        )

    def get_shadow_root(self):
        shadow_host = self.__driver.find_element(By.CSS_SELECTOR, "div.shadow-root-monetha")
        return shadow_host.shadow_root

    def click_activate_button(self):
        shadow = self.get_shadow_root()
        button = shadow.find_element(By.CSS_SELECTOR, "button.ex-ewrwf.ex-vff1s.ex-jwsuc.ex-ul0w1")
        button.click()

    @allure.step("Ждать появления ожидаемого процента кэшбэка")
    def wait_for_cashback_text(self, expected_cashback: str, timeout: int = 20):
        shadow = self.get_shadow_root()
        WebDriverWait(self.__driver, timeout).until(
            lambda d: expected_cashback in shadow.find_element(By.CSS_SELECTOR, "span.ex-qn03r").text.strip()
        )

    def get_cashback_text(self):
        shadow = self.get_shadow_root()
        cashback_elem = shadow.find_element(By.CSS_SELECTOR, "span.ex-qn03r")
        return cashback_elem.text.strip()
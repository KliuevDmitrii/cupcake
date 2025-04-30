import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

class LoginExtPage:
    """
    Этот класс предоставляет методы для выполнения действий на странице авторизации пользователя в расширении.
    """

    def __init__(self, driver: WebDriver) -> None:
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url + "/login/?extension=true"
        self.__driver = driver

    @allure.step("Перейти на страницу авторизации")
    def go(self):
        self.__driver.get(self.__url)
        WebDriverWait(self.__driver, 10).until(lambda d: len(d.window_handles) > 1)
        self.__driver.switch_to.window(self.__driver.window_handles[-1])
        self.__driver.refresh()

    @allure.step("Нажать таб Login")
    def click_tab_login(self):
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, '//div[@class="tab"]//div[@class="tab-title" and contains(text(), "Login")]'))
        ).click()

    @allure.step("Ввести почту в поле email")
    def enter_email(self, email: str):
        element = self.__driver.find_element(By.XPATH, '//input[@name="email"]')
        element.clear()
        element.send_keys(email)
        return element.text
    
    @allure.step("Ввести пароль в поле password")
    def enter_password(self, password: str):
        element = self.__driver.find_element(By.XPATH, '//input[@name="password"]')
        element.clear()
        element.send_keys(password)
        return element.text
    
    @allure.step("Нажать кнопку CONNECT")
    def click_button_connect(self):
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, '//button[contains(@class, "button") and contains(., "CONNECT")]'))
        ).click()
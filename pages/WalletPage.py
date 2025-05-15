import allure
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from configuration.ConfigProvider import ConfigProvider

class WalletPage:
    """
    Этот класс предоставляет методы для выполнения действий на странице авторизации пользователя.
    """

    def __init__(self, driver: WebDriver) -> None:
        url = ConfigProvider().get("ui", "base_url")
        self.__url = url + "/account/wallet"
        self.__driver = driver

    @allure.step("Перейти на страницу кошелька")
    def go(self):
        sleep(2)
        self.__driver.get(self.__url)

    @allure.step("Получение данных пользователя: points, level name и tier score")
    def get_user_account_data(self):
        data = {}

        try:
            points_el = self.__driver.find_element(By.CLASS_NAME, "points-wrapper").find_element(By.XPATH, ".//div")
            points_text = points_el.text.strip()
            data['points'] = int(''.join(filter(str.isdigit, points_text)))
        except Exception:
            data['points'] = None

        try:
            level_name = self.__driver.find_element(By.CLASS_NAME, "tier-badge-text")
            data['level_name'] = level_name.text.strip()
        except Exception:
            data['level_name'] = None

        try:
            tier_score_el = self.__driver.find_element(By.CLASS_NAME, "tier-score-wrapper")
            tier_score_text = tier_score_el.text.strip()
            data['tier_score'] = int(''.join(filter(str.isdigit, tier_score_text)))
        except Exception:
            data['tier_score'] = None

        print(f"WEB DATA: {data}")
        return data
        
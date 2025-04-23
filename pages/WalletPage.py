import allure
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
        self.__driver.get(self.__url)
        self.__driver.refresh()

    @allure.step("Получение данных пользователя: points, badge и tier score")
    def get_user_account_data(self):
        data = {}

        # Получение points
        try:
            points_el = self.__driver.find_element(By.CLASS_NAME, "points-wrapper").find_element(By.XPATH, ".//div")
            data['points'] = points_el.text.strip()
        except Exception:
            data['points'] = None

        # Получение badge
        try:
            badge_el = self.__driver.find_element(By.CLASS_NAME, "points-button-badge")
            data['badge'] = badge_el.text.strip()
        except Exception:
            data['badge'] = None

        # Получение tier score
        try:
            tier_score_el = self.__driver.find_element(By.CLASS_NAME, "tier-score-wrapper")
            data['tier_score'] = tier_score_el.text.strip()
        except Exception:
            data['tier_score'] = None

        return data
    
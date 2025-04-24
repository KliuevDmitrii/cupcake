from socket import timeout
import pytest
import allure
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

from api.monethaAPI import MonethaApi
from pages.LoginExtPage import LoginExtPage
from configuration.ConfigProvider import ConfigProvider
from testdate.DataProvider import DataProvider

@pytest.fixture
def browser_with_extension():
    with allure.step("Открыть и настроить браузер"):
        config = ConfigProvider()
        timeout = config.getint("ui", "timeout", fallback=5)
        browser_name = config.get("ui", "browser_name", fallback="chrome").lower()
        chrome_extension_path = config.get("ui", "chrome_extension_path", fallback=None)
        ff_extension_path = config.get("ui", "ff_extension_path", fallback=None)

        if browser_name == "chrome":
            chrome_options = ChromeOptions()

            if chrome_extension_path and os.path.isdir(chrome_extension_path):
                abs_path = os.path.abspath(chrome_extension_path)
                chrome_options.add_argument(f"--load-extension={abs_path}")
                print(f"Расширение подключено: {abs_path}")
            elif chrome_extension_path:
                print(f"Неверный путь к расширению: {chrome_extension_path}")

            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=chrome_options
            )

        elif browser_name in ["ff", "firefox"]:
            firefox_options = FirefoxOptions()

            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=firefox_options
            )

            if ff_extension_path and os.path.isfile(ff_extension_path):
                abs_path = os.path.abspath(ff_extension_path)
                driver.install_addon(abs_path, temporary=True)
                print(f"Расширение установлено: {abs_path}")
            elif ff_extension_path:
                print(f"Неверный путь к расширению: {ff_extension_path}")

        else:
            raise ValueError(f"Неизвестный браузер: {browser_name}")

        driver.implicitly_wait(timeout)
        driver.maximize_window()

        init_delay = config.getint("ui", "extension_init_wait", fallback=5)
        print(f"Ожидание {init_delay} сек. после запуска браузера")
        time.sleep(init_delay)

    yield driver

    with allure.step("Закрыть браузер"):
        driver.quit()

@pytest.fixture
def browser():
    with allure.step("Открыть и настроить браузер"):
        config = ConfigProvider()
        timeout = config.getint("ui", "timeout")

        browser_name = config.get("ui", "browser_name", fallback="chrome")
        browser_name = browser_name.lower() if browser_name else "chrome"

        if browser_name == 'chrome':
            browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif browser_name in ['ff', 'firefox']:
            browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        else:
            raise ValueError(f"Неизвестное значение browser_name: {browser_name}")

        browser.implicitly_wait(timeout)
        browser.maximize_window()

    yield browser

    with allure.step("Закрыть браузер"):
            browser.quit()

@pytest.fixture
def test_data():
        return DataProvider()

@pytest.fixture
def authorized_api_client():
    config = ConfigProvider()
    data_provider = DataProvider()

    base_url = config.get("api", "base_url")
    email = data_provider.get("email")
    password = data_provider.get("pass")
    platform = data_provider.get("platform")

    temp_api = MonethaApi(base_url, token="")

    with allure.step("Авторизация пользователя через API"):
        auth_response = temp_api.auth_user(email, password, platform)

        if "access_token" not in auth_response:
            raise Exception(f"Авторизация не удалась: {auth_response}")

        token = auth_response["access_token"]
    
    return MonethaApi(base_url, token)
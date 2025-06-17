from socket import timeout
import pytest
import allure
import time
import random
import pprint
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
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
    '''
    Фикстура для настройки браузера с расширением (Chrome, Chromium, Firefox).
    '''
    with allure.step("Открыть и настроить браузер"):
        config = ConfigProvider()
        timeout = config.getint("ui", "timeout", fallback=5)
        browser_name = config.get("ui", "browser_name", fallback="chrome").lower()
        chrome_extension_path = config.get("ui", "chrome_extension_path", fallback=None)
        ff_extension_path = config.get("ui", "ff_extension_path", fallback=None)

        if browser_name in ["chrome", "chromium"]:
            chrome_options = ChromeOptions()

            # Путь к расширению
            if chrome_extension_path and os.path.isdir(chrome_extension_path):
                abs_path = os.path.abspath(chrome_extension_path)
                chrome_options.add_argument(f"--load-extension={abs_path}")
                chrome_options.add_argument("--disable-features=ExtensionsToolbarMenu")
                print(f"Расширение подключено (папка): {abs_path}")
            elif chrome_extension_path:
                print(f"Неверный путь к расширению: {chrome_extension_path}")

            # Важно: флаги против DevToolsActivePort ошибки
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_experimental_option("detach", True)  # окно остаётся открытым

            if browser_name == "chromium":
                chrome_options.binary_location = "/usr/bin/chromium-browser"

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
    '''
    Фикстура для настройки браузера.'''
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
        '''
        Фикстура для получения тестовых данных.'''
        return DataProvider()

@pytest.fixture
def authorized_api_client() -> MonethaApi:
    '''
    Фикстура для авторизации пользователя через API и получения токена.'''
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

@pytest.fixture
def random_merchant(authorized_api_client: MonethaApi) -> dict:
    '''
    Фикстура для получения случайного мерчанта.
    '''
    merchants = authorized_api_client.get_all_merchants()

    websites_with_percent = []
    for m in merchants:
        website = m.get("website")
        percent = m.get("points", {}).get("percent", 1)
        interstitial_url = m.get("interstitialURL")
        if website:
            websites_with_percent.append((website, percent, m.get("name"), interstitial_url))

    if not websites_with_percent:
        raise ValueError("Нет доступных сайтов у мерчантов")

    raw_url, raw_percent, name, interstitial_url = random.choice(websites_with_percent)

    parsed = urlparse(interstitial_url)
    query = parse_qs(parsed.query)
    query["platform"] = ["extension"]
    new_query = urlencode(query, doseq=True)
    interstitial_url = urlunparse(parsed._replace(query=new_query))

    parsed_url = urlparse(raw_url).netloc or urlparse(raw_url).path
    clean_website = parsed_url.replace(".", " ").replace("/", " ").strip()

    cashback_value = round(raw_percent * 100, 1) if raw_percent else 0
    cashback_percent = f"{cashback_value}%"

    print(f"Выбранный URL: {raw_url}, Процент: {cashback_percent}, Interstitial URL: {interstitial_url}")

    return {
        "clean_website": clean_website,
        "cashback_percent": cashback_percent,
        "merchant_url": raw_url,
        "merchant_name": name,
        "interstitial_url": interstitial_url,
    }

@pytest.fixture
def random_merchants(authorized_api_client: MonethaApi) -> list:
    '''
    Фикстура для получения списка случайных мерчантов.
    '''
    merchants = authorized_api_client.get_all_merchants()

    websites_with_percent = []
    for m in merchants:
        website = m.get("website")
        percent = m.get("points", {}).get("percent", 1)
        name = m.get("name")
        interstitial_url = m.get("interstitialURL")
        if website:
            websites_with_percent.append((website, percent, name, interstitial_url))

    if not websites_with_percent:
        raise ValueError("Нет доступных сайтов у мерчантов")

    selected_merchants = random.sample(websites_with_percent, 4)

    merchant_data_list = []
    for raw_url, raw_percent, name, interstitial_url in selected_merchants:
        parsed_url = urlparse(raw_url).netloc or urlparse(raw_url).path
        clean_website = parsed_url.replace(".", " ").replace("/", " ").strip()

        cashback_value = round(raw_percent * 100, 1) if raw_percent else 0
        cashback_percent = f"{cashback_value}%"

        print(f"Выбранный URL: {raw_url}, Процент: {cashback_percent}, Interstitial URL: {interstitial_url}")
        
        merchant_data_list.append({
            "clean_website": clean_website,
            "cashback_percent": cashback_percent,
            "merchant_url": raw_url,
            "merchant_name": name,
            "interstitial_url": interstitial_url,
        })

    return merchant_data_list

@pytest.fixture
def random_top_merchants(authorized_api_client: MonethaApi) -> list:
    '''
    Фикстура для получения списка случайных топ-мерчантов.'''
    merchants = authorized_api_client.get_top_merchants()

    websites_with_percent = []
    for m in merchants:
        website = m.get("website")
        percent = m.get("points", {}).get("percent", 1)
        name = m.get("name")
        interstitial_url = m.get("interstitialURL")
        if website:
            websites_with_percent.append((website, percent, name, interstitial_url))

    if not websites_with_percent:
        raise ValueError("Нет доступных сайтов у мерчантов")

    selected_merchants = random.sample(websites_with_percent, 5)

    top_merchant_data_list = []
    for raw_url, raw_percent, name, interstitial_url in selected_merchants:
        parsed_url = urlparse(raw_url).netloc or urlparse(raw_url).path
        clean_website = parsed_url.replace(".", " ").replace("/", " ").strip()

        cashback_value = round(raw_percent * 100, 1) if raw_percent else 0
        cashback_percent = f"{cashback_value}%"

        print(f"Выбранный URL: {raw_url}, Процент: {cashback_percent}, Interstitial URL: {interstitial_url}")
        
        top_merchant_data_list.append({
            "clean_website": clean_website,
            "cashback_percent": cashback_percent,
            "merchant_url": raw_url,
            "merchant_name": name,
            "interstitial_url": interstitial_url,
        })
    
    print(top_merchant_data_list)

    return top_merchant_data_list

@pytest.fixture
def wishlist_merchant(authorized_api_client: MonethaApi) -> str:
    '''
    Фикстура для получения случайного мерчанта из списка желаемого (wishlist).'''
    merchants = authorized_api_client.get_wishlist()

    if not isinstance(merchants, list) or not merchants:
        raise ValueError("Список wishlist пуст или имеет неверный формат")

    selected = random.choice(merchants)
    
    print(f"Выбранный URL: https://{selected}")

    return f"https://{selected}"

@pytest.fixture
def get_user_information(authorized_api_client: MonethaApi) -> dict:
    '''
    Фикстура для получения информации о пользователе.
    '''
    user_balance = authorized_api_client.get_user_balance()
    user_progress = authorized_api_client.get_user_progress()

    approved_tokens = user_balance.get("approvedTokens")
    expired_tokens = user_balance.get("expiredTokens")

    if approved_tokens is None or expired_tokens is None:
        pytest.fail("Не удалось получить токены из API: approvedTokens или expiredTokens = None")

    if approved_tokens == 0 and expired_tokens == 0:
        pytest.fail("API вернул нулевые значения токенов: approvedTokens и expiredTokens равны 0")

    sum_balance = approved_tokens + expired_tokens

    boosts = user_progress.get("boosts")
    level_info = user_progress.get("level")

    if level_info is None or level_info.get("name") is None:
        pytest.fail("Не удалось получить уровень пользователя (level_name) из API")

    level_name = level_info.get("name")

    return {
        "sum_balance": sum_balance,
        "boosts": boosts,
        "level_name": level_name
    }
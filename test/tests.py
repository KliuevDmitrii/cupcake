from time import sleep
import allure
import pytest
import random
from urllib.parse import urlparse

from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from testdate.DataProvider import DataProvider
from pages.LoginExtPage import LoginExtPage
from pages.LoginPage import LoginPage
from pages.WalletPage import WalletPage
from api.monethaAPI import MonethaApi


@allure.title("Проверка редиректа на страницу авторизации после установки расширения в браузере")
def test_extension_redirect(browser_with_extension):
    found = False
    for handle in browser_with_extension.window_handles:
        browser_with_extension.switch_to.window(handle)
        current_url = browser_with_extension.current_url
        print("Вкладка:", current_url)

        if "monetha.io/login" in current_url and "extension=true" in current_url:
            found = True
            break

    with allure.step("Проверить, что расширение открыло страницу авторизации после установки"):
        assert found, "Расширение не открыло нужную вкладку"
        print("Расширение установилось и выполнило редирект:", browser_with_extension.current_url)

@allure.title("Проверка авторизации пользователя в расширении")
def test_auth_user_ext(browser_with_extension, test_data: dict):
    email = test_data.get("email")
    password = test_data.get("pass")

    login_page_ext = LoginExtPage(browser_with_extension)

    login_page_ext.go()
    login_page_ext.click_tab_login()
    login_page_ext.enter_email(email)
    login_page_ext.enter_password(password)

    tabs_before = browser_with_extension.window_handles
    login_page_ext.click_button_connect()

    with allure.step("Ожидание закрытия вкладки"):
        WebDriverWait(browser_with_extension, 10).until(
            lambda driver: len(driver.window_handles) < len(tabs_before)
        )

    with allure.step("Проверить, что вкладка авторизации закрылась"):
        tabs_after = browser_with_extension.window_handles
        assert len(tabs_after) < len(tabs_before), \
            f"Ожидалось, что вкладка закроется. До: {len(tabs_before)}, После: {len(tabs_after)}"

@allure.title("Проверка авторизации по API")
def test_token_is_received(authorized_api_client):
    with allure.step("Проверить что токен был получен"):
        assert authorized_api_client.token, "Токен не был получен"

@allure.title("Проверка наличия access_token, refresh_token и expires_in после авторизации")
def test_auth_user_tokens(authorized_api_client):
    test_data = DataProvider()
    email = test_data.get("email")
    password = test_data.get("pass")
    platform = test_data.get("platform")

    with allure.step("Выполнить авторизацию по API"):
        response = authorized_api_client.auth_user(email, password, platform)

    with allure.step("Проверить, что в ответе есть access_token, refresh_token и expires_in"):
        assert "access_token" in response, "В ответе отсутствует access_token"
        assert "refresh_token" in response, "В ответе отсутствует refresh_token"
        assert "expires_in" in response, "В ответе отсутствует expires_in"

# @allure.title("Проверка авторизации пользователя на сайте")
# def test_auth_user(browser, test_data: dict):
#     email = test_data.get("email")
#     password = test_data.get("pass")

#     login_page = LoginPage(browser)

#     login_page.go()
#     login_page.click_tab_login()
#     login_page.enter_email(email)
#     login_page.enter_password(password)
#     login_page.click_button_connect()


# @allure.title("Интеграционный тест: API + UI")
# def test_merchants_ui_vs_api(authorized_browser_and_token):
#     browser, token = authorized_browser_and_token
#     api = MonethaApi(base_url="https://api.monetha.io", token=token)

#     merchants = api.get_all_merchants()  # Сначала получаем переменную
#     print("Ответ API:", merchants)       # Потом её используем

#     merchant_list = merchants.get("data", [])
#     assert merchant_list, "Список магазинов пуст! Возможно, ошибка авторизации или API недоступен."
#     random_merchant = random.choice(merchants.get("data", []))
#     website = random_merchant.get("website", "")
#     percent = random_merchant.get("percent", 0)

#     domain = urlparse(website).netloc.replace(".", " ")
#     cashback_percent = f"{round(percent * 100)}%"

#     with allure.step(f"Выполняем поиск в Google по магазину: {domain}"):
#         browser.switch_to.new_window("tab")
#         browser.get("https://www.google.com")
#         search_input = WebDriverWait(browser, 10).until(
#             EC.presence_of_element_located((By.NAME, "q"))
#         )
#         search_input.send_keys(f"{domain} Monetha cashback")
#         search_input.send_keys(Keys.ENTER)

#     with allure.step("Находим нужный элемент с процентом кешбэка на странице"):
#         cashback_element = WebDriverWait(browser, 15).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, f"//div[contains(@class,'shadow-root-monetha')]//span[contains(text(), '{cashback_percent}')]")
#             )
#         )
#         assert cashback_element is not None, f"Элемент с {cashback_percent} не найден"
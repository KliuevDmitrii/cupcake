from time import sleep
import allure
import pytest
import random
from urllib.parse import urlparse

from selenium.webdriver.chrome.webdriver import WebDriver
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from datetime import datetime

from testdate.DataProvider import DataProvider
from pages.LoginExtPage import LoginExtPage
from pages.SearchPage import SearchPage
from pages.ExtensionPage import ExtensionPage
from pages.LoginPage import LoginPage
from pages.WalletPage import WalletPage
from api.monethaAPI import MonethaApi


@allure.title("Проверка редиректа на страницу авторизации после установки расширения в браузере")
def test_extension_redirect(browser_with_extension: WebDriver):
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
def test_auth_user_ext(browser_with_extension: WebDriver, test_data: dict):
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

@allure.title("Проверка ответа со списком мерчанов")
def test_list_merch(authorized_api_client):
    with allure.step("Получить список всех магазинов"):
        response = authorized_api_client.get_all_merchants()

    assert isinstance(response, list), "Ожидался список мерчантов"

    with allure.step("Проверить наличие обязательных полей у каждого мерчанта"):
        for merchant in response:
            assert "affiliateURL" in merchant, f"Нет поля affiliateURL у: {merchant.get('name', merchant)}"
            assert "interstitialURL" in merchant, f"Нет поля interstitialURL у: {merchant.get('name', merchant)}"
            if "percent" not in merchant:
                print(f"[!] У мерчанта {merchant.get('name', merchant)} отсутствует percent — пропускаем")
                continue
            assert "percent" in merchant, f"Нет поля percent у: {merchant.get('name', merchant)}"
            assert "website" in merchant, f"Нет поля website у: {merchant.get('name', merchant)}"

@allure.title("Проверка наличия серпа и процента кэшбэка мерчанта для авторизованного пользователя в поисковике")
def test_existence_serp(browser_with_extension: WebDriver, test_data: dict, random_merchant):
    email = test_data.get("email")
    password = test_data.get("pass")
    test_data.get("platform")

    login_page_ext = LoginExtPage(browser_with_extension)
    search_page = SearchPage(browser_with_extension)

    login_page_ext.go()
    login_page_ext.click_tab_login()
    login_page_ext.enter_email(email)
    login_page_ext.enter_password(password)
    login_page_ext.click_button_connect()

    window_handles = browser_with_extension.window_handles
    if window_handles:
        browser_with_extension.switch_to.window(window_handles[0])

    search_page.go()
    search_query = random_merchant["clean_website"]
    search_page.enter_merch_name(search_query)
    search_page.wait_for_serp()

    expected_cashback = random_merchant["cashback_percent"]

    with allure.step(f"Проверить наличие серпа и правильность процента кэшбэка ({expected_cashback})"):
        search_page.verify_serp_cashback(expected_cashback)


@pytest.mark.parametrize("merchant_data_index", [0, 1, 2, 3])
@allure.title("Проверка наличия серпа и процента кэшбэка у нескольких рандомных мерчантов")
def test_existence_serp_multiple(browser_with_extension: WebDriver, test_data: dict, random_merchants, merchant_data_index):
    email = test_data.get("email")
    password = test_data.get("pass")
    test_data.get("platform")

    merchant_data = random_merchants[merchant_data_index]

    login_page_ext = LoginExtPage(browser_with_extension)
    search_page = SearchPage(browser_with_extension)

    login_page_ext.go()
    login_page_ext.click_tab_login()
    login_page_ext.enter_email(email)
    login_page_ext.enter_password(password)
    login_page_ext.click_button_connect()

    window_handles = browser_with_extension.window_handles
    if window_handles:
        browser_with_extension.switch_to.window(window_handles[0])

    search_page.go()

    search_query = merchant_data["clean_website"]
    search_page.enter_merch_name(search_query)
    search_page.wait_for_serp()

    expected_cashback = merchant_data["cashback_percent"]

    with allure.step(f"Проверить наличие серпа и правильность процента кэшбэка ({expected_cashback}) для {merchant_data['merchant_name']}"):
        search_page.verify_serp_cashback(expected_cashback)

@allure.title("Проверка наличия popup и процента кэшбэка на странице мерчанта для авторизованного пользователя")
def test_popup_on_merchant_page(
    browser_with_extension: WebDriver,
    test_data: dict,
    random_merchant: dict
):
    email = test_data.get("email")
    password = test_data.get("pass")

    login_page = LoginExtPage(browser_with_extension)
    login_page.go()
    login_page.click_tab_login()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_connect()

    merchant_url = random_merchant["merchant_url"]
    expected_cashback = random_merchant["cashback_percent"]

    print(merchant_url)

    browser_with_extension.execute_script(f"window.open('{merchant_url}');")
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    browser_with_extension.refresh()
    popup = ExtensionPage(browser_with_extension)
    try:
        popup.wait_for_popup()
        popup.wait_for_cashback_text(expected_cashback)
        cashback_text = popup.get_cashback_text()

        with allure.step("Проверить наличие серпа и правильность процента кэшбэка"):
            assert expected_cashback == cashback_text, (
                f"Ожидался кэшбэк {expected_cashback}, но найден {cashback_text}"
            )

    except TimeoutException:
        screenshot = browser_with_extension.get_screenshot_as_png()
        allure.attach(screenshot, name="popup_not_found", attachment_type=allure.attachment_type.PNG)
        pytest.fail("Попап расширения не появился или кэшбэк не отобразился вовремя")

# def test_popup_on_merchant_page(browser_with_extension: WebDriver, test_data: dict, authorized_api_client: MonethaApi):
#     email = test_data.get("email")
#     password = test_data.get("pass")

#     login_page = LoginExtPage(browser_with_extension)
#     login_page.go()
#     login_page.click_tab_login()
#     login_page.enter_email(email)
#     login_page.enter_password(password)
#     login_page.click_button_connect()

#     merchants = authorized_api_client.get_all_merchants()
#     available = []
#     for m in merchants:
#         website = m.get("website")
#         points = m.get("points", {})
#         percent = points.get("percent")
#         name = m.get("name")
#         if website and percent:
#             available.append((website, percent, name))
#     selected = random.choice(available)
#     print(selected)
#     merchant_url, percent, name = selected
#     expected_cashback = f"{round(percent * 100, 1)}%"

#     browser_with_extension.execute_script(f"window.open('{merchant_url}');")
#     browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

#     browser_with_extension.refresh()

#     popup = ExtensionPage(browser_with_extension)
#     try:
#         popup.wait_for_popup()
#         popup.wait_for_cashback_text(expected_cashback)
#         cashback_text = popup.get_cashback_text()

#         with allure.step("Проверить наличие серпа и правильность процента кэшбэка"):
#             assert expected_cashback == cashback_text, (
#                 f"Ожидался кэшбэк {expected_cashback}, но найден {cashback_text}"
#             )

#     except TimeoutException:
#         screenshot = browser_with_extension.get_screenshot_as_png()
#         allure.attach(screenshot, name="popup_not_found", attachment_type=allure.attachment_type.PNG)
#         pytest.fail("Попап расширения не появился или кэшбэк не отобразился вовремя")



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
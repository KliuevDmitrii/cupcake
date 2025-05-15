from time import sleep
import allure
import pytest
import random
from urllib.parse import urlparse

from selenium.webdriver.chrome.webdriver import WebDriver
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
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

    WebDriverWait(browser_with_extension, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

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

    print(f"[DEBUG] Merchant URL: {merchant_url}")
    print(f"[DEBUG] Expected Cashback: {expected_cashback}")

    browser_with_extension.execute_script(f"window.open('{merchant_url}');")
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    WebDriverWait(browser_with_extension, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    browser_with_extension.close()
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    browser_with_extension.execute_script(f"window.open('{merchant_url}');")
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    WebDriverWait(browser_with_extension, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    popup = ExtensionPage(browser_with_extension)

    try:
        popup.wait_for_popup()
        with allure.step(f"Проверить наличие попапа и правильность процента кэшбэка ({expected_cashback})"):
            popup.verify_popup_cashback(expected_cashback)

    except TimeoutException:
        screenshot = browser_with_extension.get_screenshot_as_png()
        allure.attach(screenshot, name="popup_or_cashback_timeout", attachment_type=allure.attachment_type.PNG)
        pytest.fail("Попап расширения не появился или кэшбэк не отобразился вовремя")


@allure.title("Проверка наличия popup и процента кэшбэка на странице мерчанта для авторизованного пользователя")
def test_popup_on_merchant_page_2(
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

    print(f"[DEBUG] Merchant URL: {merchant_url}")
    print(f"[DEBUG] Expected Cashback: {expected_cashback}")

    browser_with_extension.execute_script(f"window.open('{merchant_url}');")
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    WebDriverWait(browser_with_extension, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    browser_with_extension.close()
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    browser_with_extension.execute_script(f"window.open('{merchant_url}');")
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    WebDriverWait(browser_with_extension, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    popup = ExtensionPage(browser_with_extension)

    try:
        popup.wait_for_popup()
        popup.wait_for_cashback_text(expected_cashback)
        cashback_text = popup.get_cashback_text()

        with allure.step("Проверить наличие popup и правильность процента кэшбэка"):
            assert expected_cashback == cashback_text, (
                f"Ожидался кэшбэк {expected_cashback}, но найден {cashback_text}"
            )

    except TimeoutException:
        screenshot = browser_with_extension.get_screenshot_as_png()
        allure.attach(screenshot, name="popup_not_found", attachment_type=allure.attachment_type.PNG)
        pytest.fail("Попап расширения не появился или кэшбэк не отобразился вовремя")

@allure.title("Проверка наличия popup и процента кэшбэка на странице рандомных мерчантов для авторизованного пользователя")
@pytest.mark.parametrize("merchant_data_index", [0, 1, 2, 3])
def test_popup_on_random_merchants_page(
    browser_with_extension: WebDriver,
    test_data: dict,
    random_merchants: list,
    merchant_data_index: int
):
    email = test_data.get("email")
    password = test_data.get("pass")

    login_page = LoginExtPage(browser_with_extension)
    login_page.go()
    login_page.click_tab_login()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_connect()

    merchant = random_merchants[merchant_data_index]
    merchant_url = merchant["merchant_url"]
    expected_cashback = merchant["cashback_percent"]

    browser_with_extension.execute_script(f"window.open('{merchant_url}');")
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    WebDriverWait(browser_with_extension, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    browser_with_extension.close()
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    browser_with_extension.execute_script(f"window.open('{merchant_url}');")
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    WebDriverWait(browser_with_extension, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    popup = ExtensionPage(browser_with_extension)
    browser_with_extension.refresh()
    try:
        popup.wait_for_popup()
        popup.wait_for_cashback_text(expected_cashback)
        cashback_text = popup.get_cashback_text()

        with allure.step("Проверить наличие popup и корректность процента кэшбэка"):
            assert cashback_text == expected_cashback, (
                f"Ожидался кэшбэк {expected_cashback}, но найден {cashback_text}"
            )
    except TimeoutException:
        screenshot = browser_with_extension.get_screenshot_as_png()
        allure.attach(screenshot, name=f"popup_not_found_{merchant_data_index}", attachment_type=allure.attachment_type.PNG)
        pytest.fail("Попап не появился или кэшбэк не отобразился вовремя")

@allure.title("Проверка наличия popup и процента кэшбэка на странице рандомных TOP мерчантов для авторизованного пользователя")
@pytest.mark.parametrize("top_merchant_data_index", [0, 1, 2, 3, 4])
def test_popup_on_random_top_merchants_page(
    browser_with_extension: WebDriver,
    test_data: dict,
    random_top_merchants: list,
    top_merchant_data_index: int
):
    email = test_data.get("email")
    password = test_data.get("pass")

    login_page = LoginExtPage(browser_with_extension)
    login_page.go()
    login_page.click_tab_login()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_connect()

    merchant = random_top_merchants[top_merchant_data_index]
    merchant_url = merchant["merchant_url"]
    expected_cashback = merchant["cashback_percent"]

    browser_with_extension.execute_script(f"window.open('{merchant_url}');")
    browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    popup = ExtensionPage(browser_with_extension)
    browser_with_extension.refresh()
    try:
        popup.wait_for_popup()
        popup.wait_for_cashback_text(expected_cashback)
        cashback_text = popup.get_cashback_text()

        with allure.step("Проверить наличие popup и корректность процента кэшбэка"):
            assert cashback_text == expected_cashback, (
                f"Ожидался кэшбэк {expected_cashback}, но найден {cashback_text}"
            )
    except TimeoutException:
        screenshot = browser_with_extension.get_screenshot_as_png()
        allure.attach(screenshot, name=f"popup_not_found_{top_merchant_data_index}", attachment_type=allure.attachment_type.PNG)
        pytest.fail("Попап не появился или кэшбэк не отобразился вовремя")

@allure.title("Проверка редиректа на affiliate страницу при активации кэшбэка на странице мерчанта")
def test_redirect_to_affiliate(
    browser_with_extension: WebDriver,
    test_data: dict,
    random_merchant: dict
):
    email = test_data.get("email")
    password = test_data.get("pass")
    merchant_url = random_merchant["merchant_url"]
    interstitial_url = random_merchant["interstitial_url"]

    with allure.step("Авторизация пользователя"):
        login_page = LoginExtPage(browser_with_extension)
        login_page.go()
        login_page.click_tab_login()
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_button_connect()

        WebDriverWait(browser_with_extension, 20).until(
            lambda d: len(d.window_handles) == 1
        )
        browser_with_extension.switch_to.window(browser_with_extension.window_handles[0])

    with allure.step("Открытие страницы мерчанта"):
        browser_with_extension.execute_script(f"window.open('{merchant_url}');")
        WebDriverWait(browser_with_extension, 20).until(
            lambda d: len(d.window_handles) == 2
        )
        browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])
        
        WebDriverWait(browser_with_extension, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    with allure.step("Активация кэшбэка и проверка редиректа"):
        extension = ExtensionPage(browser_with_extension)
        
        browser_with_extension.refresh()
        
        merchant_tab = browser_with_extension.current_window_handle

    with allure.step("Нажать кнопку активации кэшбэка"):
        try:
                extension.click_activate_button()
        except Exception as e:
                pytest.fail(f"Не удалось нажать кнопку активации: {str(e)}")

        WebDriverWait(browser_with_extension, 10).until(
                lambda d: merchant_tab not in d.window_handles
            )
            
        browser_with_extension.switch_to.window(browser_with_extension.window_handles[1])
            
        current_url = extension.get_current_url()

        with allure.step("Проверить что URL содержит 'monetha.io/affiliate'"):
            assert "monetha.io/affiliate" in current_url, (
                    f"Ожидался URL содержащий 'monetha.io/affiliate', получен '{current_url}'"
                )
            assert "platform=extension" in current_url, (
                    "В URL отсутствует параметр 'platform=extension'"
                )

        
    # with allure.step("Проверка статуса 'Активировано' в попапе"):
    #     try:
    #         extension.wait_for_popup()
    #         is_active = extension.is_cashback_activated()
    #         assert is_active, "Кэшбэк не отображается как активированный в попапе"
    #     except Exception as e:
    #         pytest.fail(f"Не удалось проверить статус 'Активировано' в попапе: {str(e)}")
    
@allure.title("Проверка наличия popup на странице потенциального мерчанта для авторизованного пользователя")
def test_popup_on_wishlist_merchant_page(
    browser_with_extension: WebDriver,
    test_data: dict,
    wishlist_merchant: str
):
    email = test_data.get("email")
    password = test_data.get("pass")

    login_page = LoginExtPage(browser_with_extension)
    login_page.go()
    login_page.click_tab_login()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_connect()

    merchant_url = wishlist_merchant
    

    for i in range(5):
        browser_with_extension.execute_script(f"window.open('{merchant_url}');")
        browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

        WebDriverWait(browser_with_extension, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        if i == 4:
            with allure.step("Проверка наличия попапа с текстом 'Come here often?'"):
                try:
                    popup = ExtensionPage(browser_with_extension)
                    popup.wait_for_popup()
                    popup.check_popup_header()
                    
                    assert popup is not None, "Попап не появился на пятой странице."
                    allure.attach(browser_with_extension.get_screenshot_as_png(), name="Popup Screenshot", attachment_type=allure.attachment_type.PNG)
                except Exception as e:
                    pytest.fail(f"Не удалось найти попап: {str(e)}")

        # browser_with_extension.close()

        # browser_with_extension.switch_to.window(browser_with_extension.window_handles[-1])

    with allure.step("Завершение теста"):
        assert True, "Тест прошел успешно."

@allure.title("Проверка баланса пользователя в расширении через API и в web личном кабинете")
def test_balance_user(browser: WebDriver,
    test_data: dict,
    get_user_information: dict):
    email = test_data.get("email")
    password = test_data.get("pass")

    login_page_web = LoginPage(browser)

    login_page_web.go()
    login_page_web.click_tab_login()
    login_page_web.enter_email(email)
    login_page_web.enter_password(password)
    login_page_web.click_button_connect()

    wallet_page = WalletPage(browser)

    wallet_page.go()

    web_data =  wallet_page.get_user_account_data()
    sum_balance_ui = web_data.get("points")
    boosts_ui = web_data.get("tier_score")
    level_name_ui = web_data.get("level_name")

    api_data = get_user_information

    sum_balance_api = api_data["sum_balance"]
    boosts_api = api_data["boosts"]
    level_name_api = api_data["level_name"]

    with allure.step("Проверить совпадение данных на странице wallet и ответ от API расширения"):
        assert sum_balance_ui == sum_balance_api, \
            f"Баланс токенов не совпадает: UI={sum_balance_ui}, API={sum_balance_api}"

        assert level_name_ui == level_name_api, \
            f"Уровень не совпадает: UI={level_name_ui}, API={level_name_api}"

        assert boosts_ui == boosts_api, \
            f"Список бустов не совпадает: UI={boosts_ui}, API={boosts_api}"
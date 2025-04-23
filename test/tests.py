from time import sleep
import allure
import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.LoginExtPage import LoginExtPage
from pages.LoginPage import LoginPage
from pages.WalletPage import WalletPage


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

@allure.title("Проверка авторизации пользователя на сайте")
def test_auth_user(browser, test_data: dict):
    email = test_data.get("email")
    password = test_data.get("pass")

    login_page = LoginPage(browser)

    login_page.go()
    login_page.click_tab_login()
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_button_connect()
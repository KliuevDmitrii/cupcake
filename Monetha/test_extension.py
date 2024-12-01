from time import sleep
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.ExtensionTester import ExtensionTester

@pytest.fixture(scope="session")
def browser():
    tester = ExtensionTester("/home/dmitriik/Документы/Cupcake/Monetha/monetha-extension-chrome-v-1.1.10")
    tester.setup_browser_with_extension()
    yield tester.driver
    tester.quit_browser()

def test_extension_installed(browser):
    browser.get("chrome://extensions/")
    body_text = browser.find_element(By.TAG_NAME, "body").text
    assert "Расширения" in body_text or "Extensions" in body_text

@pytest.mark.parametrize("url, merchant", [
    ("https://www.google.com/", "sephora")
])
def test_serp_to_google(browser, url, merchant):
    tester = ExtensionTester()
    tester.driver = browser
    tester.open_new_tab(url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    tester.search_merchant(merchant)
    assert tester.verify_cashback_element(), "Элемент с ID 'monetha-sr' отсутствует на странице."


# @pytest.mark.parametrize("url", [
#     "https://www.macys.com/"
# ])
# def test_open_new_tab(browser, url):
#     tester = ExtensionTester()
#     tester.driver = browser
#     tester.open_new_tab(url)
#     sleep(3)
#     assert url in tester.driver.current_url, f"Expected URL '{url}' but got '{tester.driver.current_url}'"


# @pytest.mark.parametrize("email, password", [
#     ("dimitrikliuev@gmail.com", "Qwerty12345!")
# ])
# def test_login_extension(browser, email, password):
#     extension_id = "ffpljcgoppimojikmiiehchklbmkdnae"
#     login_page = ExtensionTester()
#     login_page.driver = browser
#     login_page.open_extension_popup(extension_id)
    
#     try:
#         login_page.click_button_login_in_extension()
#         login_page.input_email(email)
#         login_page.input_password(password)
#         login_page.click_connect()

#         # Проверка успешного логина
#         assert "Welcome" in browser.page_source  # Замените на актуальное условие
#     except Exception as e:
#         print(f"Ошибка: {str(e)}")

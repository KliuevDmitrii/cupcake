import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from pages.ExtensionTester import ExtensionTester

@pytest.fixture
def browser():
    tester = ExtensionTester("/path/to/extension")
    tester.setup_browser_with_extension()
    yield tester.driver
    tester.quit_browser()

def test_extension_installed(browser):
    browser.get("chrome://extensions/")
    assert "Extensions" in browser.title
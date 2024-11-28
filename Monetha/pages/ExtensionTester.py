from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ExtensionTester:
    def __init__(self, extension_path):
        self.extension_path = extension_path
        self.driver = None

    def setup_browser_with_extension(self):
       extension_path = "/home/dmitriik/Документы/Cupcake/Monetha"
       chrome_options = Options()
       chrome_options.add_argument(f"--load-extension={extension_path}")

       driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
       driver.get("https://www.example.com")
    
    def quit_browser(self):
        if self.driver:
            self.driver.quit()

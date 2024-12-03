from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ExtensionTester:
    def __init__(self, extension_path=None):
        self.extension_path = extension_path
        self.driver = None

    def setup_browser_with_extension(self):
        chrome_options = Options()
        if self.extension_path:
            chrome_options.add_argument(f"--load-extension={self.extension_path}")
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get("https://www.example.com")
    
    def open_new_tab(self, url="about:blank"):
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def search_merchant(self, merchant=""):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(merchant)
        search_box.send_keys(Keys.RETURN)
    
    def check_text_in_shadow_root(self):
        try:
            shadow_host = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "css-селектор-shadow-host"))
            )
            
            shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", shadow_host)
            element = shadow_root.find_element(By.CSS_SELECTOR, "span.ex-zu1yt")
            text_content = element.text
            assert "You can receive cashback from Monetha for purchases from the store up to" in text_content
            print("Текст найден!")
        except TimeoutException:
            print("Элемент не найден.")
        except AssertionError:
            print("Текст не найден.")
        except NoSuchElementException:
            print("Элемент внутри shadow-root не найден.")



    # def open_extension_popup(self, extension_id):
    #     popup_url = f"chrome-extension://{extension_id}/popup.html"
    #     self.driver.get(popup_url)
    #     self.driver.switch_to.window(self.driver.window_handles[-1])
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//button[text()='Login']"))
    # )

    # def click_button_login_in_extension(self):
    #     login_button_xpath = "//button[text()='Login']"
    #     WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, login_button_xpath))
    #     ).click()

    # def input_email(self, email):
    #     email_field_xpath = "//input[@name='email' and @type='email']"
    #     WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located((By.XPATH, email_field_xpath))
    #     ).clear()
    #     self.driver.find_element(By.XPATH, email_field_xpath).send_keys(email)

    # def input_password(self, password):
    #     password_field_xpath = "//input[contains(@class, 'password-field') and @name='password' and @type='password']"
    #     WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located((By.XPATH, password_field_xpath))
    #     ).clear()
    #     self.driver.find_element(By.XPATH, password_field_xpath).send_keys(password)

    # def click_connect(self):
    #     connect_button_xpath = "//div[contains(@class, 'button-text') and text()='CONNECT']"
    #     WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, connect_button_xpath))
    #     ).click()

    def quit_browser(self):
        if self.driver:
            self.driver.quit()

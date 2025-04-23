import allure
import requests
import json

class MonethaApi:
    """
    Этот класс предоставляет методы для выполнения действий с API
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    @allure.step("Авторизоваться")
    def auth_user(self, email, password):
        body = {
            "email": email,
            "password": password
        }
        
        path = f"{self.base_url}/user/v1/email/signin"
        headers = {"x-user-authorization": f"Bearer {self.token}"}

        resp = requests.post(path, json=body, headers=headers)

        print(f"Status Code: {resp.status_code}, Response Text: {resp.text}")

        try:
            response_json = resp.json()
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка декодирования JSON. Ответ API: {resp.text}")

        access_token = response_json.get("access_token")
        if access_token:
            self.token = access_token
            self._update_token_in_file(access_token)
            print("Новый токен сохранён в test_data.json")

        return response_json

    @allure.step("Перезаписать access_token в test_data.json")
    def _update_token_in_file(self, token: str):
        try:
            with open("test_data.json", "r+", encoding="utf-8") as file:
                data = json.load(file)
                data["access_token"] = token
                file.seek(0)
                json.dump(data, file, indent=2)
                file.truncate()
        except Exception as e:
            print(f"Ошибка при обновлении test_data.json: {e}")

    @allure.step("Получить баланс пользователя")
    def get_user_balance(self):
        url = f"{self.base_url}/wallet/balance"
        headers = {"x-user-authorization": f"Bearer {self.token}"}
        resp = requests.get(url, headers=headers)
        return resp.json()

    @allure.step("Получить прогресс пользователя")
    def get_user_progress(self):
        url = f"{self.base_url}/user/progress"
        headers = {"x-user-authorization": f"Bearer {self.token}"}
        resp = requests.get(url, headers=headers)
        return resp.json()
    
    @allure.step("Получить список всех магазинов")
    def get_all_merchants(self):
        url = f"{self.base_url}/merchants"
        headers = {"x-user-authorization": f"Bearer {self.token}"}
        resp = requests.get(url, headers=headers)
        return resp.json()

    @allure.step("Получить топ магазинов по кешбэку")
    def get_top_merchants(self, source="web"):
        url = f"{self.base_url}/merchants/high-rewards"
        headers = {"x-user-authorization": f"Bearer {self.token}"}
        params = {"source": source}
        resp = requests.get(url, headers=headers, params=params)
        return resp.json()

    @allure.step("Получить wishlist пользователя")
    def get_wishlist(self):
        url = f"{self.base_url}/merchants/wishlist"
        headers = {"x-user-authorization": f"Bearer {self.token}"}
        resp = requests.get(url, headers=headers)
        return resp.json()
    
    @allure.step("Добавить магазин в кешбэк wishlist")
    def add_to_cashback_wishlist(self, store_domain: str):
        url = f"{self.base_url}/cashback-wishlist"
        headers = {
            "x-user-authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {"store_domain": store_domain}
        resp = requests.post(url, json=data, headers=headers)
        return resp.json()


    @allure.step("Получить информацию о магазине по домену")
    def get_merchant_info(self, domain: str):
        url = f"{self.base_url}/merchant/lookup"
        headers = {"x-user-authorization": f"Bearer {self.token}"}
        params = {"domain": domain}
        resp = requests.get(url, headers=headers, params=params)
        return resp.json()
    
    



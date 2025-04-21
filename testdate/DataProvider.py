import json

my_file = open('test_data.json')
global_data = json.load(my_file)

class DataProvider:

    def __init__(self) -> None:
        self.data = global_data
        
    def get(self, prop: str, default=None) -> str:
        """Получить строковое значение параметра, вернуть default, если параметр отсутствует."""
        return self.data.get(prop, default)

    def getint(self, prop: str, default=0) -> int:
        """Получить целочисленное значение параметра, вернуть default, если параметр отсутствует."""
        try:
            return int(self.data.get(prop, default))
        except (ValueError, TypeError):
            print(f"Ошибка преобразования {prop} в int, возвращаю {default}")

    def get_token(self) -> str:
        """Получить токен."""
        return self.get("token")
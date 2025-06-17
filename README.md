# Monetha ext

## Шаги запуска

1. **Клонировать проект**

   ```bash
   git clone https://github.com/KliuevDmitrii/cupcake.git
   cd cupcake
   ```

2. **Создать и активировать виртуальное окружение**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Установить зависимости**

   ```bash
   pip install -r requirements.txt
   ```

4. **Создать файл конфигурации **``** в папке **``

   > Этот файл находится в `.gitignore`, нужно создать вручную.

   ```ini
   [ui]  
   base_url=https://www.monetha.io
   search_url=https://www.bing.com
   timeout=4
   chrome_extension_path=./ext/monetha-extension-chrome-v-1.1.16
   ff_extension_path=./ext/monetha-extension-firefox-v-1.1.16.zip
   extension_init_wait=1

   # chrome | ff | chromium
   browser_name=chromium

   [api]  
   base_url=https://api.monetha.io
   ```

5. **Создать файл с тестовыми данными **``** в папке **``

   > ⚠️ Этот файл также в `.gitignore`, создайте вручную.

   ```json
   {
     "email": "example@example.com",
     "pass": "XXXXXX",
     "platform": "web",
     "access_token": "...",
     "refresh_token": "...",
     "token": "..."
   }
   ```

6. **Запустить тесты**

   ```bash
   pytest
   ```

7. **Сгенерировать Allure отчёт**

   ```bash
   allure generate allure-files -o allure-report
   allure open allure-report
   ```

---

## Стек технологий

- `pytest` — запуск тестов
- `selenium` — автоматизация браузера
- `webdriver-manager` — установка драйверов
- `requests` — API-запросы
- `allure` — отчёты
- `configparser` — конфигурационные файлы
- `json` — работа с тестовыми данными

---

## Структура проекта

```
/test           # UI и API тесты
/page           # PageObject-описание страниц
/api            # API-хелперы (Monetha API)
/configuration  # Настройки и провайдер
  └─ test_config.ini (local config)
/testdata       # Тестовые данные
  └─ test_data.json (email, tokens)
/ext            # Расширения для Chrome и Firefox
```

---

## Полезные ссылки

- [Markdown шпаргалка](https://www.markdownguide.org/basic-syntax/)
- [Генератор .gitignore](https://www.toptal.com/developers/gitignore)

---

## Ручная установка библиотек

```bash
pip install pytest
pip install selenium
pip install webdriver-manager
pip install allure-pytest
```
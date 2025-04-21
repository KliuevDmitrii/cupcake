# Monetha ext

### Шаги
1. Склонировать проект 'https://github.com/KliuevDmitrii/cupcake.git'
2. Установить зависимости 'pip3 install > -r requirements.txt'
3. Запустить тесты 'pytest'
4. Сгенерировать отчет 'allure generate allure-files -o allure-report'
5. Открыть отчет 'allure open allure-report'

### Стек:
- pytest
- selenium
- webdriver manager 
- requests
- allure
- configparser
- json

### Струткура:
- ./test - тесты
- ./page - описание страниц
- ./api - хелперы для работы с API
- ./configuration - провайдер настроек
    - test_config.ini - настройки для тестов
- ./testdata - провайдер тестовых данных
    - test_data.json

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)


### Библиотеки
- pip3 install pytest
- pip3 install selenium
- pip3 install webdriver-manager
- pip3 install allure-pytest
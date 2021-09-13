**Описание**

Web-приложение для простого учета посещенных ссылок

**Библиотеки**

python = "^3.8"

Django = "^3.2.7"

redis = "^3.5.3"

**Для работы с приложением**

- example.env переименовать в .env и раскомментировать содержимое
- git clone https://github.com/pvladimir1989/funbox_test.git
- cd funbox_test
- docker-compose up

**Примеры**

Запрос POST на добавление ссылок:

curl -X POST "http://localhost:8000/visited_links" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"links\":[\"https://ya.ru\",\"https://ya.ru?q=123\",\"funbox.ru\",\"https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor\"]}"

Запрос GET для получения доменов:

curl -X GET "http://localhost:8000/visited_domains?from=1&to=100000000000" -H "accept: application/json"

**Тесты**

Используется unittest. Запускается из докера

- docker exec -it funbox_test_web_1 sh
- cd ..
- python manage.py test


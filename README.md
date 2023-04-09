![CI](https://github.com/DFyand/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Описание проекта api_yamdb
### Краткое описание проекта
Пример работы workflow с четырьмя задачями
### Описание задач workflow
- tests - проверка тестами
- build_and_push_to_docker_hub - сборка и отправка в docker hub
- deploy - развернуть на боевоес сервере
- send_message - отправка сообщения о готовности в телеграм
### Секретные переменные
- user - имя пользователя
- password - пароль
- HOST - ip боевого сервера
- SSH_KEY - приватный ключ для доступа
- PASSPHRASE - фраза дял доступа

База данных:
- DB_ENGINE - указываем, что работаем с postgresql
- DB_NAME - имя базы данных
- POSTGRES_USER - логин для подключения к базе данных
- POSTGRES_PASSWORD - пароль для подключения к БД (установите свой)
- DB_HOST - название сервиса (контейнера)
- DB_PORT - порт для подключения к БД

Телеграм:
- TELEGRAM_TO - адрес доставки
- TELEGRAM_TOKEN - токен бота

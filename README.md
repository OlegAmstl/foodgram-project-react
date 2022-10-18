<!--START_SECTION:badges-->

<!--END_SECTION:badges-->

### Проект Foodgram

Footgram кулинарный портал, на котором вы можете найти рецепты как старой проверенной классики вреде "Котлеток с пюрешкой", так и совершенно новых блюд и даже экзотических. Так же вы сами сможете поделиться своими рецептами, чтобы и остальные могли приобщиться к изысканной гастрономии.


### Технологии в проекте:
- Python 3.10
- Django 2.2.20
- Django REST Flamework 3.12.4
- gunicorn 20.0.4
- nginx
- PostgreSQL 13
- Docker 20.10.18
- Docker Compose v2.4.1
- React

### Как запустить проект:
* Для работы проекта необходимо, чтоб на рабочей станции были установлены Docker и Docker Compose указанных выше версий или новее.
* Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:OlegAmstl/foodgram-project-react.git
cd foodgram-project-react
```
* Перейти в папку с infra:
```
cd infra
```
* Заполнить файл с переменными окружения
```
# Параметры для работы контейнера с db
POSTGRES_DB=<название БД>
POSTGRES_USER=<SQL пользователь БД>
POSTGRES_PASSWORD=<пароль для SQL User>
```
```
# Параметры для работы контейнера web
# Настройки соедиения с DB для Django, нужно заполнить только DB_NAME, DB_USER, DB_PASS, ALLOWED_HOST, остальные настройки менять не рекомендуется
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<название БД>
DB_USER=<SQL пользователь БД>
DB_PASS=<пароль для SQL User>
DB_HOST=db
DB_PORT=5432
# Режим DEBUG в Django, 1 - включен, 0 - отключен.
DEBUG=0
ALLOWED_HOST=<IP или доменое имя рабочей станции, на которой планируется запускать проект>
```
* В файле default.conf выставить IP рабочей станции (127.0.0.1 заменить на IP или доменное имя рабочей станции, на которой планируется запускать проект)
```
server_name <ваш IP>;
```

 Запустить docker-compose нижеуказанной командой, cборка может занять некоторое время. По окончании работы docker-compose сообщит, что контейнеры скачаны и запущены:
```
sudo docker-compose up -d
```
* После запуска подключиться к http://<ваш IP>/admin/ браузером, убедиться что интерфейс администратора Django доступен.

* Выполнить миграции следующей командой:
```
sudo docker-compose exec web python manage.py migrate
```
* Создать суперпользователя:
```
sudo docker-compose exec web python manage.py createsuperuser
```
* Собрать статику в соответствующем томе
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
* Можно заполнить базу предустановленным списком ингредиентов и тегов:
```
sudo docker-compose exec web python manage.py add_tags_from_data
sudo docker-compose exec web python manage.py add_ingidients_from_data
```
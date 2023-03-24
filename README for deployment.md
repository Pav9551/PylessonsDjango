# Домашнее задание по Django (python lesson 28)

## Это инструкция по развертыванию Web-сервиса.
#### Сервис парсит сайт https://edadeal.ru/ и записывает данные по скидкам в базу данных
```
```
- Сервис парсит данные по скидкам с сайта https://edadeal.ru/ по магазинам Лента, Пятерочка и Перекресток;
- Список интересующих нас товаров загружается из списка, который формирует пользователь;
- Далее,сервис выбирает из списка товаров со скидками интересующие нас товары и записывает в базу данных через ORM;
- Пользователь может отправить список товаров себе на почту.
```
```
#### Шаблон сайта взят с https://startbootstrap.com/theme/clean-blog
#### Диаграмма развертывания представлена на рисунке
![Alt-текст](https://github.com/Pav9551/PylessonsDjango/blob/nu-28-postgre-edadeal/UML_Deployment.png "Deployment")
## Оглавление

1. [Подключение по ssh](#Подключение-по-ssh)
2. [Установка docker-compose](#Установка-docker-compose)
3. [Установка сервиса](#Установка-сервиса)
4. [Установка gunicorn](#Установка-gunicorn)
5. [Установка nginx](#Установка-nginx)
6. [Перезагрузка сервисов и установка локалей](#Перезагрузка-сервисов-и-установка-локалей)
## Подключение по ssh
Тестирование сервиса проводилось на операционной системе Ubuntu 20.04 c python 3.8</sup>

```curl   
ssh-keygen -R 123.456.789.90 (если нужно очистить ключ) 
ssh root@123.456.789.90
```
## Установка docker-compose
 - Для установки docker-compose необходимо:
```curl   
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker

sudo userdel -f deploy
sudo useradd -G adm -p password -s /bin/bash deploy
passwd deploy
usermod -aG root deploy
usermod -aG sudo deploy
usermod -aG docker deploy
groups deploy
su - deploy

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
cd /home/deploy
sudo mkdir docker-compose
sudo apt -y install mc
```
 - содержимое  docker-compose.yaml

```curl  
version: '3.7'
services:
  postgres:
    container_name: postgres
    image: postgres:14.0-alpine
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./postgres/data:/var/lib/postgresql/data
      - ./postgres/etc/postgresql:/etc/postgresql
      - ./postgres/var/log/postgresql:/var/log/postgresql
    environment:
      - "POSTGRES_USER=user"
      - "POSTGRES_PASSWORD=password"
      - "POSTGRES_DB=database"
    restart: always
    ports:
      - 5352:5432
    volumes: 
      - ./postgres/docker_postgres_init.sql:/docker-entrypoint-initdb.d/docker_postgres_init.sql
    #networks:
      #- backend
  pgadmin:
    container_name: pgadmin4_container
    image: dpage/pgadmin4:5.5
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: email@admin.com
      PGADMIN_DEFAULT_PASSWORD: password
      PGADMIN_LISTEN_PORT: 80
    ports:
      - "8080:80"
    depends_on: 
      - postgres
```

 - содержимое ./postgres/docker_postgres_init.sql

```curl  
CREATE USER user2 WITH PASSWORD 'PASSWORD';
GRANT pg_read_all_data TO user2;


CREATE DATABASE db;
CREATE USER django with NOSUPERUSER PASSWORD 'nu123456';
GRANT ALL PRIVILEGES ON DATABASE db TO django;

ALTER ROLE django SET CLIENT_ENCODING TO 'UTF8';
ALTER ROLE django SET default_transaction_isolation TO 'READ COMMITTED';
ALTER ROLE django SET TIME ZONE 'Europe/Moscow';
```


```curl 
./restart.sh
/docker-compose$ docker-compose ps
exit 
```
## Установка сервиса
 - Для работы сервиса необходимо: создать виртуальное окружение, скачать файлы с репозитория и установить необходимые пакты
```curl   
apt update && apt upgrade -y
python3 --version
mkdir edadeal 
cd edadeal
apt install python3.8-venv
python3 -m venv env
source env/bin/activate
git clone https://github.com/Pav9551/PylessonsDjango
cd PylessonsDjango
pip3 install -r requirements.txt
pip install psycopg2-binary
```
 - сконфигурировать учетку yandex почты для подключения по SMTP
 - в папке PylessonsDjango создать .env c ключом и другими переменными среды:
```curl
SECRET_KEY='django-insecure-SECRET_KEY'
NAME='db'
ENGINE='django.db.backends.postgresql'
USER_PG='USER_PG'
PASSWORD='PASSWORD'
HOST='123.456.789.90'
PORT='5352'

EMAIL_HOST_USER = '*****@yandex.ru'
EMAIL_HOST_PASSWORD = 'PASSWORD'
 ```
## Установка gunicorn
 - Gunicorn позволяет подключить сервис к nginx
```curl   
- установить
pip install gunicorn
- Тестовый запуск проекта
gunicorn blog.wsgi (из папки проекта)
- Регистрация gunicorn как сервиса (сеть, сокет)
sudo nano /etc/systemd/system/gunicorn.service
```
 - содержимое gunicorn.service
```curl 
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/deploy/PylessonsDjango/blog
ExecStart=/home/deploy/PylessonsDjango/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/deploy/PylessonsDjango/blog/blog.sock blog.wsgi

[Install]
WantedBy=multi-user.target
 ```
 - добавить указанного в файле пользователя в группу www-data
```curl
sudo usermod -aG www-data root
groups root
```
## Установка nginx
 - Nginx позволяет увеличить скорость обработки статического контента
```curl 
- установка:
sudo apt install nginx
service nginx status
- насройка nginx:
cd /etc/nginx/sites-available/
- перенаправление запросов на сокет гуникорна
nano default
```
- содержимое default
```curl 
server {
    listen 80;
    server_name 123.456.789.90;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/deploy/PylessonsDjango/blog;
    }

    location /media/ {
        root /home/deploy/PylessonsDjango/blog;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/deploy/PylessonsDjango/blog/blog.sock;
    }
}
```
## Перезагрузка сервисов и установка локалей
```curl 
service gunicorn restart
service nginx restart
service nginx status

dpkg-reconfigure locales
```
Были проблемы с кодировкой символов, я
включил все локали, перезагрузил и выключил все локали.
Перезагрузил и включл нужные локали.
Перезагрузил и все заработало.













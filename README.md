# Домашнее задание по Django (python lesson 20)


## Перезапуск:

1. python manage.py migrate blogapp zero --fake
2. удалить 0001_initial.py и др 000...
3. удалить db.sqlite3
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver

## Web-сервис демонстрирует работу Django framework.
#### Сервис парсит сайт https://edadeal.ru/ и записывает данные по скидкам в базу данных
```
```
- В сервисе реализовано REST API, принимающее на вход POST запросы с содержимым вида {"questions_num": integer} ;
- После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов;
- Далее, полученные ответы сохраняются в базе данных, причем сохранена должна быть следующая информация: 1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса. В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
- Ответом на Post запрос должен быть предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.
```
```
## Оглавление

1. [Требования к операционной системе](#Требования-к-операционной-системе)
3. [Установка веб-сервиса](#Установка-веб-сервиса)
4. [Пример использования](#Пример-использования)

## Требования к операционной системе
Тестирование сервиса проводилось на операционной системе Windows 7 </sup>

## Установка веб-сервиса
 - Для установки веб-сервиса необходимо скопировать содержимое репозитория на диск:
```curl   
git clone https://github.com/Pav9551/PylessonsDjango/tree/nu20-orm
```
 - перейти в папку с файлом restart.sh;
```curl   
cd flask_postgres
```
 - сделать файл restart.sh исполняемым:
```curl 
 sudo chmod +x restart.sh
 ```
 - запустить файл:
```curl 
 ./restart.sh
```
 - дождаться конца установки;
 - проверить состояние контейнеров командой:
```curl 
 docker-compose ps
```

 - убедиться, что подняты сервисы согласно документу docker-compose.yaml.

## Пример использования
Чтобы протестировать веб-сервис необходимо отправить Post запрос. Для этого необходимо знать IP адрес хоста, порт и шаблон запроса:
```curl
curl http://127.0.0.1:4999/questions -X POST -H "Content-Type: application/json" -d '{"questions_num": 5}'
```
```Python
#Python
import requests
endpoint = f'http://127.0.0.1:4999/questions'
headers = {
    "Content-Type": "application/json"
}
data = {"questions_num": 5}
r = requests.post(endpoint, json = data, headers = headers)#
print(r.status_code)
print(r.text)

```
Для подключения к базе данных PostgreSQL с помощью программы Navicat 15 for PostgreSQL извне используйте следующие данные:
```
```
 - Хост: {внешний IP хоста}
 - Порт: 5352
 - DB: main
 - USER: root
 - PASSWORD: 1234
```
```
<a name="myfootnote1">1</a> Информация по установке сервисов docker и docker-compose взята с сайта https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru и https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04 (step1):










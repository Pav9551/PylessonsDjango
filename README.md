# Домашнее задание по Django (python lesson 30)

## Web-сервис демонстрирует работу ORM Django framework.
#### Сервис парсит сайт https://edadeal.ru/ и записывает данные по скидкам в базу данных
```
```
- Сервис парсит данные по скидкам с сайта https://edadeal.ru/ по магазинам Лента, Пятерочка и Перекресток
- Список интересующих нас товаров загружается из goods.xlsx
- Далее,сервис выбирает из списка товаров со скидками интересующие нас товары и записывает в базу данных через ORM.

```
```
#### Шаблон сайта взят с https://startbootstrap.com/theme/clean-blog
#### Диаграмма прецидентов системы представлена на рисунке
![Alt-текст](https://github.com/Pav9551/PylessonsDjango/blob/master/uses_case.png "use case")
## Оглавление

1. [Требования к операционной системе](#Требования-к-операционной-системе)
2. [Установка веб-сервиса](#Установка-веб-сервиса)
3. [Пример использования](#Пример-использования)

## Требования к операционной системе
Тестирование сервиса проводилось на операционной системе Windows 7 c python 3.7</sup>

## Установка веб-сервиса
 - Для установки веб-сервиса необходимо скопировать содержимое репозитория на диск:
```curl   
git clone https://github.com/Pav9551/PylessonsDjango
```
 - Для работы сервиса необходимо поставить зависимости
```curl   
pip3 install -r requirements.txt
```
 - рядом с requirements.txt создать файл .env c ключом:
```curl 
SECRET_KEY = 'django-insecure-1234567890'
 ```

 - перейти в папку blog с файлом manage.py:
```curl 
cd blog
 ```

 - сбросить все миграции:
```curl 
python manage.py migrate blogapp zero --fake
```
 - удалить файлы миграции в каталоге migrations:
```curl 
0001_initial.py и др. 000...
```
 - создать файлы миграции командой:
```curl 
python manage.py makemigrations
```
 - сделать миграции в базу командой:
```curl 
python manage.py migrate
```
 - создать суперпользователя:
```curl 
python manage.py createsuperuser
```
## Пример использования
Чтобы протестировать веб-сервис необходимо:
 - загрузить данные в базу:
```curl 
python manage.py fill_goods
```
 - запустить сервер:
```curl 
python manage.py runserver
```
 - перейти по адресу и посмотреть данные Merchandise через админку:
```curl 
http://127.0.0.1:8000/admin/
```

если порт забился:
```curl 
sudo fuser -k 8000/tcp
```


если порт забился:
```curl 
sudo fuser -k 8000/tcp
```
Можно собрать статистику по товарам и пользователям через API:
```curl 
http://127.0.0.1:8000/api/
```
автоматически рисовать диаграмму отношений классов модели:
```curl 
python manage.py graph_models -a -o models.png
```
https://russianblogs.com/article/80721384625/









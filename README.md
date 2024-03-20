# __Курсовая работа Базы данных__

### получение вакансий с сайта HH.ru по заданным параметрам
### и занесение их в базу данных

___

### Как работать:
Внести свои данные в файл `config.ini`  
Обязательна к заполнению секция [postgresql], остальное можно использовать по  
умолчанию. Файл `config.ini` прилагается в папке `conf`

[postgresql] # данные для подключения к БД  
host=свои данные  
user=свои данные  
password=свои данные  
port=свои данные

[hh_ru] # по желанию можно изменить параметры запроса  
areas=113  
only_with_salary=True  
per_page=100  

[employees_id] # здесь id работодателей тоже можно изменить  
3529=sber  
3127=megafon  
3388=gazprombank  
2180=ozon  
80=alphabank  
1740=yandex  
4219=tele2  
15478=vk  
39305=gazpromneft  
1373=aeroflot  

Запуск программы с `main.py`  
После запуска, программа предложит ввести имя создаваемой базы данных.  
Создание и заполнение таблиц происходит автоматически. Дождитесь окончания заполнения таблиц.
Далее высветится меню команд каждая из которых вызывает определенную функцию для работы с таблицами.  
Результаты работы функций будут выведены на экран.


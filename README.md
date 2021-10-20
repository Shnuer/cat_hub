# cat_hub
### Приложение для загрузки картинок

#### Начальные приготовления:
1. Иметь установленый MySQL и созданную базу с пользователям для проекта. В файле my_config задать значения для вашей базы
 
        mysql+pymysql://USER_NAME:USER_PASSWORD@HOST/DATABASE_NAME

2. Установить необходимые пакеты из *requirements.txt*

        pip3 install -r requirements.txt

3. Для автоматического создания запустить файл *init_db.py*

        python init_db.py

по оканчанию работы скрипта в базе данных должны появиться необходимые таблицы.
##### Запуск
1. Для запуска необходимо установить значение переменой *FLASK_APP* имени проекта *cat_hub*

    Для windows:

        set FLASK_APP=cat_hub

    Для Linux:

        export FLASK_APP=cat_hub

2. Для запуска приложения использовать команду:


        flask run


# ProductLab Стасевич Дарья Викторовна

1) Клонируем проект https://github.com/Darya-Stasevich/ProductLab.git

Задание №1 Запустить питоновский файлик test1.py

Задание №2 (для Windows)

2) Создаем виртуальное окружение python -m venv venv
3) Активируем виртуальное окружение venv/Scripts/activate
4) Устанавливаем зависимости pip install -r requirements.txt
5) Выполняем миграции python manage.py makemigrations,
python manage.py migrate
6) Запускаем проект python manage.py runserver
7) Переходим на локальный сервер http://127.0.0.1:8000/
8) Переходим на нужный endpoint "http://127.0.0.1:8000/get_article/" (API принимающее один артикул)
либо "http://127.0.0.1:8000/get_articles_list/" (API принимающее файл формата xlsx)

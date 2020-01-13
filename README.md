# # All-to-the-bottom-parser
Парсер логов для интернет магазина "Все на дно!"

Язык программирования: python 3

База данных: MySQL

Для визуализации используется Jupyter Notebook

# Для установки необходимых библиотек:

pip3 install -r requirements.txt

# Для запуска парсера и заполнения бд: 

python3 parser.py

Логи загружаются около часа (из-за медленной работы питона с бд)

Можно не ждать и сразу запустить веб-приложение - бд уже заполнена.

# Чтобы запустить веб-приложение и юпитер ноутбук введите:

export FLASK_APP=app.py

flask run 

jupyter nbconvert --execute Visualisation.ipynb

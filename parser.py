import pandas as pd
import numpy as np

import sqlite3
import requests

from db_wrapper import request_db

db = request_db('database')

# очистка и подготовка логов к преобразованию в датафрейм
cleared_lines = []
with open('logs.txt') as f:
    for line in f.readlines():
        cleared_line = " ".join(line.replace('|','').split()).split()
        cleared_line[6] = cleared_line[6].replace('https://all_to_the_bottom.com/', '')
        if cleared_line[6] == '':
            cleared_line[6] = 'index'
        cleared_line[1] = cleared_line[1] + ' ' + cleared_line[2]
        cleared_lines.append(cleared_line)

# преобразование в датафрейм для упрощения работы с большим объемом данных
df = pd.DataFrame(cleared_lines, columns=[0, 'date', 'time', 'id', 4, 'ip', 'action']).drop([0, 4], axis=1)
df = df.replace('', np.nan).dropna()
df.reset_index(drop=True, inplace=True)

# создание mysql базы данных
conn = sqlite3.connect("database")
cursor = conn.cursor()

cursor.execute("""DROP TABLE IF EXISTS Users""")
cursor.execute("""DROP TABLE IF EXISTS Actions""")
cursor.execute("""DROP TABLE IF EXISTS Transasction""")
cursor.execute("""DROP TABLE IF EXISTS Products""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    ip TEXT NOT NULL UNIQUE,
                    country TEXT
                    );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS Actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    path TEXT NOT NULL,
                    dtime DATETIME,
                    u_id INTEGER REFERENCES Users (id)
                    );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS Transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    finished BOOL DEFAULT 'False',
                    dtime DATETIME,
                    u_id INTEGER REFERENCES Users (id)
                    );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS Products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    name TEXTs NOT NULL
                    );
               """)

data = cursor.fetchall()
conn.close()

# парсинг стран из айпи
# из-за несовершенства выбранного ною сервиса многие юзеры получат страну = Undefiend
for i, ip in enumerate(df.ip.unique()):
    try:
        response = requests.get(f'http://ipinfo.io/{ip}?token=75c7c09e5f27cd')
        country = response.json()['country']
    except:
        country = 'Undefiend'
    db.request_insert_two('Users', 'ip, country', ip, country)

# парсинг таблицы Product
for i, item in enumerate(df.action.unique()):
    if item.count('/') == 2:
        product = item.split('/')
        try:
            print('Trying to put ', product, ' into table Products')
            db.request_insert_two('Products', 'category, name', product[0], product[1])
        except:
            print('Err: Product already in database\n')

# парсинг таблицы м
for i, item in enumerate(df.action):
    if 'pay?' in item:
        u_id = db.request_select('id', 'Users', 'ip', df.ip[i])
        db.request_insert_two('Transactions', 'dtime, u_id', df.date[i], u_id[0][0])
    elif 'pay_' in item:
        u_id = db.request_select('id', 'Users', 'ip', df.ip[i])
        t_id = db.request_select_one('id', 'Transactions', 'u_id', u_id[0][0], 'dtime')
        db.request_update('Transactions', 'finished', True, 'id', t_id[0][0])
    u_id = db.request_select('id', 'Users', 'ip', df.ip[i])
    db.request_insert_three('Actions', 'path, dtime, u_id', df.action[i], df.date[i], u_id[0][0])

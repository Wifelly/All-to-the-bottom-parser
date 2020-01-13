import sqlite3
from pprint import pprint as print

from flask import Flask, request, Response, redirect, jsonify

from db_wrapper import request_db

app = Flask(__name__)
db = request_db('database')

@app.route('/first')
def first():
    dct = {}
    response = []
    cities = db.request_select_join('*', 'Users', 'Actions')
    print(cities[0])
    print(cities[0][0])
    for item in cities:
        if item[2] in dct.keys():
            dct[item[2]] += 1
        else:
            dct[item[2]] = 1
    for item in dct.keys():
        response.append((dct[item], item))
    response.sort(key=lambda tup: tup[0])
    return jsonify(response)

@app.route('/second')
def second():
    lst = []
    dct = {}
    lst_sorted = []
    actions = db.request_select_join('*', 'Users', 'Actions')
    for item in actions:
        if (item[4].count('/') >= 1) and ('pay' not in item[4]):
            lst.append(item[2] + ' ' + item[4].split('/')[0])
    for item in lst:
        if item in dct.keys():
            dct[item] += 1
        else:
            dct[item] = 1
    for item in dct.keys():
        lst_sorted.append((dct[item], item))
    lst_sorted.sort(key=lambda tup: tup[0])
    lst_cat = []
    lst_cou = []
    for item in lst_sorted[::-1]:
        if item[1].split()[1] not in lst_cat:
            lst_cat.append(item[1].split()[1])
            lst_cou.append(item[1].split()[0])
    response = []
    for i, item in enumerate(lst_cat):
        response.append(item + ' ' + lst_cou[i])
    response = response[::-1]
    return jsonify(response)

@app.route('/second_visual')
def second_visual():
    lst = []
    dct = {}
    response = []
    actions = db.request_select_join('*', 'Users', 'Actions')
    for item in actions:
        if (item[4].count('/') > 1) and ('pay' not in item[4]):
            lst.append(item[2] + ' ' + item[4].split('/')[0])
    for item in lst:
        if item in dct.keys():
            dct[item] += 1
        else:
            dct[item] = 1
    for item in dct.keys():
        response.append([dct[item], item])
    response.sort(key=lambda tup: tup[0])
    return jsonify(response)

@app.route('/third')
def third():
    lst = []
    dct = {}
    response = []
    actions = db.request_select('path, dtime', 'Actions')
    for item in actions:
        if (item[0].count('/') >= 1) and ('pay' not in item[0]):
            lst.append(item[0].split('/')[0] + ' ' + item[1].split()[1][:2])
    for item in lst:
        if item in dct.keys():
            dct[item] += 1
        else:
            dct[item] = 1
    for item in dct.keys():
        response.append(item + ' ' + str(dct[item]))
    response.sort()
    return jsonify(response)

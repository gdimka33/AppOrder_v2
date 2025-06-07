import os
import sqlite3
from База_данных.инициализация_бд import инициализировать_базу

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

СПРАВОЧНИК_ЗВАНИЙ = []
СПРАВОЧНИК_ДОЛЖНОСТЕЙ = []
СПРАВОЧНИК_ПОДРАЗДЕЛЕНИЙ = []
СПРАВОЧНИК_ПОСТОВ = []
СПРАВОЧНИК_ТИПОВ_НАРЯДОВ = []
СПРАВОЧНИК_ОФИЦЕРОВ = []
СПРАВОЧНИК_КУРСАНТОВ = []

def загрузить_все_справочники():
    global СПРАВОЧНИК_ЗВАНИЙ, СПРАВОЧНИК_ДОЛЖНОСТЕЙ, СПРАВОЧНИК_ПОДРАЗДЕЛЕНИЙ, СПРАВОЧНИК_ПОСТОВ, СПРАВОЧНИК_ТИПОВ_НАРЯДОВ, СПРАВОЧНИК_ОФИЦЕРОВ, СПРАВОЧНИК_КУРСАНТОВ
    if not os.path.exists(DB_PATH):
        инициализировать_базу()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    СПРАВОЧНИК_ЗВАНИЙ = [dict(row) for row in cur.execute('SELECT * FROM звания')]
    СПРАВОЧНИК_ДОЛЖНОСТЕЙ = [dict(row) for row in cur.execute('SELECT * FROM должности')]
    СПРАВОЧНИК_ПОДРАЗДЕЛЕНИЙ = [dict(row) for row in cur.execute('SELECT * FROM подразделения')]
    СПРАВОЧНИК_ПОСТОВ = [dict(row) for row in cur.execute('SELECT * FROM посты')]
    СПРАВОЧНИК_ТИПОВ_НАРЯДОВ = [dict(row) for row in cur.execute('SELECT * FROM типы_нарядов')]
    СПРАВОЧНИК_ОФИЦЕРОВ = [dict(row) for row in cur.execute('SELECT * FROM офицеры')]
    СПРАВОЧНИК_КУРСАНТОВ = [dict(row) for row in cur.execute('SELECT * FROM курсанты')]
    conn.close()

from sqlite3 import connect
from lib.utility.console import printc
from lib.utility.time import hour


con = connect("./data/db/database.db", check_same_thread=False)
cur = con.cursor()


def commit():
    printc("[DB]:", f"{hour()} database commit", 0)
    con.commit()


def create():
    with open('./lib/bot/create_db.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    cur.executescript(sql_script)
    con.commit()


def zelle(query, *values):
    cur.execute(query, tuple(values))
    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def spalte(query, *values):
    cur.execute(query, tuple(values))
    return [i[0] for i in cur.fetchall()]


def zeile(query, *values):
    cur.execute(query, tuple(values))
    return cur.fetchone()


def zeilen(query, *values):
    cur.execute(query, tuple(values))
    return cur.fetchall()


def execute(command, *values):
	cur.execute(command, tuple(values))


def execute_many(query, set):
    cur.executemany(query, set)


def close():
    con.close()




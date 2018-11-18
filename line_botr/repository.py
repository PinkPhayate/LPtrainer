import sqlite3
from contextlib import closing
from datetime import datetime as dt

DB_PATH = 'sqlite.db'
def create_table():
    record_query = """
    CREATE TABLE IF NOT EXISTS training_record(
        id INTEGER AUTO INCREMENT PRIMARY KEY,
        user_id INTEGER NOT NULL ,
        tr_date TEXT NOT NULL,
        tr_name TEXT NOT NULL ,
        tr_weight INTEGER,
        tr_rep INTEGER NOT NULL,
        tr_set INTEGER NOT NULL
		);
    """

    kind_query = """
    CREATE TABLE IF NOT EXISTS training_kind(
        id INTEGER AUTO INCREMENT PRIMARY KEY,
        user_id INTEGER NOT NULL ,
        tr_name TEXT NOT NULL
    );
    """

    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute(kind_query)
        con.execute(record_query)
        con.commit()

def insert_record(uid, tr_name, tr_strength):
    ary = tr_strength.split(' ')
    tr_rep = ary[0]
    tr_set = ary[1]
    tr_weight = ary[2] if 2 < len(ary) else 0
    datetime_string = dt.now().strftime("%Y-%m-%d")

    query = """
        INSERT INTO training_record (
            user_id, tr_date, tr_name, tr_weight, tr_rep, tr_set)
                VALUES ('{}', {}, '{}', {}, {}, {});

    """.format(uid, datetime_string, tr_name, tr_weight, tr_rep, tr_set)
    print(query)
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute(query)
        con.commit()

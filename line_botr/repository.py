import sqlite3
from sqlalchemy import desc
from contextlib import closing
from datetime import datetime as dt
from line_botr.training import Record
from line_botr.training import Training
from flaskr  import db
DB_PATH = 'sqlite.db'
def create_table():
    record_query = """
    CREATE TABLE IF NOT EXISTS training_record(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL ,
        tr_date TEXT NOT NULL,
        tr_name TEXT NOT NULL ,
        tr_weight INTEGER,
        tr_rep INTEGER NOT NULL,
        tr_set INTEGER NOT NULL
		);

        # Postgres
        CREATE TABLE training_record(
    	id    SERIAL primary key,
        user_id   TEXT       NOT NULL,
        tr_date   TEXT       NOT NULL,
        tr_name   TEXT        NOT NULL,
        tr_weight INTEGER,
        tr_rep INTEGER NOT NULL,
        tr_set INTEGER NOT NULL);

    """

    kind_query = """
    CREATE TABLE IF NOT EXISTS training_kind(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL ,
        tr_name TEXT NOT NULL
    );

    # Postgres
    CREATE TABLE training_kind(
	id    SERIAL primary key,
    user_id   TEXT       NOT NULL,
    tr_name TEXT NOT NULL);
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
    rec = Record(uid, datetime_string, tr_name, tr_weight, tr_rep, tr_set)
    db.session.add(rec)
    db.session.commit()

def get_records(uid):
    datetime_string = dt.now().strftime("%Y-%m-%d")
    print(datetime_string)
    return db.session.query(Record).\
            filter(Record.tr_date==datetime_string).\
            limit(10).\
            all()


def get_training_menu(uid):
    return db.session.query(Training).\
            order_by(desc( Training.id)).\
            limit(10).\
            all()

def insert_tr_menu(uid, tr_name):
    training = Training(uid, tr_name)
    db.session.add(training)
    db.session.commit()

def drop_record(input_attr):
    db.session.query(Record).\
        filter(Record.id==input_attr).\
        delete()
    db.session.commit()

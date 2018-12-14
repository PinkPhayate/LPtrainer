from sqlalchemy import desc
from contextlib import closing
from datetime import datetime as dt
from line_botr.training import Record
from line_botr.training import Training
from line_botr.session import StatusSession
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

        # Postgres
        CREATE TABLE session_table(
        user_id       TEXT       primary key,
        action_mode   TEXT,
        tr_name       TEXT,
        tr_strength   TEXT,
        last_datetime   TIMESTAMP NOT NULL);

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

def insert_record(uid, tr_name, ary):
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

def get_session_record(user_id):
    return db.session.query(StatusSession).\
            filter(StatusSession.user_id==user_id).\
            limit(1).\
            all()

def insert_session_record(sess):
    # drop_session_record(sess.user_id)
    db.session.add(sess)
    db.session.commit()

def drop_session_record(user_id):
    db.session.query(StatusSession).\
        filter(StatusSession.user_id==user_id).\
        delete()
    db.session.commit()

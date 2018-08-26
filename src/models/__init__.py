import psycopg2
import os


DB_NAME = "msgs_server"
DB_URI = os.environ.get('SERVER_DB_URI')  # postgresql://postgres@localhost
DB_COMPLETE_URI = "/".join([DB_URI, DB_NAME])


def create_db(db_name=DB_NAME, db_uri=DB_URI):
    with psycopg2.connect(db_uri) as db_con:
        db_con.autocommit = True
        sql = "CREATE DATABASE {}".format(db_name)
        with db_con.cursor() as curs:
            curs.execute(sql)


def nuke_db(db_name=DB_NAME, db_uri=DB_URI):
    with psycopg2.connect(db_uri) as db_con:
        db_con.autocommit = True
        sql = "DROP DATABASE {}".format(db_name)
        with db_con.cursor() as curs:
            curs.execute(sql)


def create_users_table(db_complete_uri=DB_COMPLETE_URI):
    with psycopg2.connect(db_complete_uri) as db_con:
        sql = """CREATE TABLE Users(
            id SERIAL,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255),
            hashed_password VARCHAR(80) NOT NULL,
            PRIMARY	KEY(id)
        )"""
        with db_con.cursor() as curs:
            curs.execute(sql)


def create_messages_table(db_complete_uri=DB_COMPLETE_URI):
    with psycopg2.connect(db_complete_uri) as db_con:
        sql = """CREATE TABLE Messages(
            id SERIAL,
            from_id INTEGER NOT NULL,
            to_id INTEGER NOT NULL,
            msg_text VARCHAR(255),
            creation_date TIMESTAMP NOT NULL DEFAULT NOW(),
            PRIMARY	KEY(id),
            FOREIGN	KEY(from_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN	KEY(to_id) REFERENCES Users(id) ON DELETE CASCADE
        )"""
        with db_con.cursor() as curs:
            curs.execute(sql)


if __name__ == '__main__':
    nuke_db()
    create_db()
    create_users_table()
    create_messages_table()
    pass

import psycopg2
import os


def create_db(db_name, db_uri):
    with psycopg2.connect(db_uri) as db_con:
        db_con.autocommit = True
        sql = "CREATE DATABASE {}".format(db_name)
        with db_con.cursor() as curs:
            curs.execute(sql)


def nuke_db(db_name, db_uri):
    with psycopg2.connect(db_uri) as db_con:
        db_con.autocommit = True
        sql = "DROP DATABASE {}".format(db_name)
        with db_con.cursor() as curs:
            curs.execute(sql)


def create_users_table(db_name, db_uri):
    with psycopg2.connect(db_uri) as db_con:
        # db_con.autocommit = True
        sql = """CREATE TABLE Users(
            id SERIAL,
            email VARCHAR(255) NOT NULL UNIQUE,
            username VARCHAR(255) NOT NULL UNIQUE,
            hashed_password VARCHAR(80) NOT NULL
        )"""
        with db_con.cursor() as curs:
            curs.execute(sql)


if __name__ == '__main__':
    db_name = "msgs_server"
    DB_URI = os.environ.get('SERVER_DB_URI')   # postgresql://postgres@localhost

    create_db(db_name=db_name, db_uri=DB_URI)
    create_users_table(db_name=db_name, db_uri="/".join([DB_URI, db_name]))

    # nuke_db(db_name=db_name, db_uri=DB_URI)


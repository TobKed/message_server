import psycopg2
import os


def create_db(db_name, db_conf):
    with psycopg2.connect() as db_con:
        db_con.autocommit = True
        sql = "CREATE DATABASE {}".format(db_name)
        with db_con.cursor() as curs:
            curs.execute(sql)


def nuke_db(db_name, db_conf):
    with psycopg2.connect() as db_con:
        db_con.autocommit = True
        sql = "DROP DATABASE {}".format(db_name)
        with db_con.cursor() as curs:
            curs.execute(sql)


if __name__ == '__main__':
    DB_URI = os.environ.get('MSGS_SERVER_DB_URI')
    create_db("msgs_server", DB_URI)

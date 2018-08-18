import psycopg2
from psycopg2.extras import RealDictCursor
from . import DB_COMPLETE_URI


class Messege:
    __id = None
    from_id = None
    to_id = None
    msg_text = ""
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = None
        self.to_id = None
        self.msg_text = ""
        self.creation_date = None

    def __repr__(self):
        return f"Messege() # id={self.id}, from_id={self.from_id}, to_id={self.to_id}," \
               f" msg_text='{self.msg_text}', creation_date={self.creation_date}"

    @property
    def id(self):
        return self.__id

    def save_to_db(self):
            with psycopg2.connect(DB_COMPLETE_URI) as db_con:
                with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                    if self.__id == -1:
                        sql = """INSERT INTO Messeges(from_id, to_id, msg_text) VALUES(%s, %s, %s) RETURNING id"""
                        values = (self.from_id, self.to_id, self.msg_text)
                        curs.execute(sql, values)
                        self.__id = curs.fetchone().get('id')
                        return True
                    else:
                        sql = """UPDATE Messeges SET from_id=%s, to_id=%s, msg_text=%s WHERE id=%s"""
                        values = (self.from_id, self.to_id, self.msg_text, self.id)
                        curs.execute(sql, values)
                        return True

    @staticmethod
    def load_messege_by_id(user_id):
        with psycopg2.connect(DB_COMPLETE_URI) as db_con:
            with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, from_id, to_id, msg_text, creation_date FROM Messeges WHERE id=%s"""
                curs.execute(sql, (user_id, ))
                data = curs.fetchone()
                if data:
                    loaded_message = Messege()
                    loaded_message._Messege__id = data.get('id')
                    loaded_message.from_id = data.get('from_id')
                    loaded_message.to_id = data.get('to_id')
                    loaded_message.msg_text = data.get('msg_text')
                    loaded_message.creation_date = data.get('creation_date')
                    return loaded_message
                else:
                    return None

    @staticmethod
    def load_all_messeges():
        rv = []
        with psycopg2.connect(DB_COMPLETE_URI) as db_con:
            with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, from_id, to_id, msg_text, creation_date FROM Messeges"""
                curs.execute(sql)
                for row in curs.fetchall():
                    loaded_message = Messege()
                    loaded_message._Messege__id = row.get('id')
                    loaded_message.from_id = row.get('from_id')
                    loaded_message.to_id = row.get('to_id')
                    loaded_message.msg_text = row.get('msg_text')
                    loaded_message.creation_date = row.get('creation_date')
                    rv.append(loaded_message)
        return rv

    @staticmethod
    def load_all_messeges_for_user(user_id):
        rv = []
        with psycopg2.connect(DB_COMPLETE_URI) as db_con:
            with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, from_id, to_id, msg_text, creation_date FROM Messeges WHERE id=%s"""
                curs.execute(sql, (user_id, ))
                for row in curs.fetchall():
                    loaded_message = Messege()
                    loaded_message._Messege__id = row.get('id')
                    loaded_message.from_id = row.get('from_id')
                    loaded_message.to_id = row.get('to_id')
                    loaded_message.msg_text = row.get('msg_text')
                    loaded_message.creation_date = row.get('creation_date')
                    rv.append(loaded_message)
        return rv

    def delete(self):
        with psycopg2.connect(DB_COMPLETE_URI) as db_con:
            with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """DELETE FROM Messege WHERE id=%s"""
                curs.execute(sql, (self.__id,))
                self._Messege__id = -1
                return True

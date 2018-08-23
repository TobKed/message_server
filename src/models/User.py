import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
from . import DB_COMPLETE_URI


class User:
    __id = None
    __hashed_password = None
    username = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    def __repr__(self):
        return f"User() # id={self.id}, username='{self.username}'. email='{self.email}'"

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    @hashed_password.setter
    def hashed_password(self, password):
        if len(password) >= 8:
            self.__hashed_password = str(User.hash_password(password), 'utf-8')
        else:
            print("Password to short. Minimum length is 8 characters.")

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_password(password, hashed):
        return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(hashed, 'utf-8'))

    def set_new_password(self, old_pass, old_pass_hashed, new_pass, new_pass_confirm):
        if self.check_password(old_pass, old_pass_hashed) is not None and new_pass == new_pass_confirm:
            self.hashed_password = new_pass
            return True
        else:
            print("Wrong password or new password do not match")

    def save_to_db(self):
            with psycopg2.connect(DB_COMPLETE_URI) as db_con:
                with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                    if self.__id == -1:
                        sql = """INSERT INTO Users(username, email, hashed_password) VALUES(%s, %s, %s) RETURNING id"""
                        values = (self.username, self.email, self.hashed_password)
                        curs.execute(sql, values)
                        self.__id = curs.fetchone().get('id')
                        return True
                    else:
                        sql = """UPDATE Users SET username=%s, email=%s, hashed_password=%s WHERE id=%s"""
                        values = (self.username, self.email, self.hashed_password, self.id)
                        curs.execute(sql, values)
                        return True

    @staticmethod
    def load_user_by_id(user_id):
        with psycopg2.connect(DB_COMPLETE_URI) as db_con:
            with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, username, email, hashed_password FROM users WHERE id=%s"""
                curs.execute(sql, (user_id, ))
                data = curs.fetchone()
                if data:
                    loaded_user = User()
                    loaded_user.__id = data.get('id')
                    loaded_user.username = data.get('username')
                    loaded_user.email = data.get('email')
                    loaded_user._User__hashed_password = data.get('hashed_password')
                    return loaded_user
                else:
                    return None

    @staticmethod
    def load_user_by_name(username):
        with psycopg2.connect(DB_COMPLETE_URI) as db_con:
            with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, username, email, hashed_password FROM users WHERE username=%s"""
                curs.execute(sql, (username, ))
                data = curs.fetchone()
                if data:
                    loaded_user = User()
                    loaded_user.__id = data.get('id')
                    loaded_user.username = data.get('username')
                    loaded_user.email = data.get('email')
                    loaded_user._User__hashed_password = data.get('hashed_password')
                    return loaded_user
                else:
                    return None

    @staticmethod
    def load_all_users():
        rv = []
        with psycopg2.connect(DB_COMPLETE_URI) as db_con:
            with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """SELECT id, username, email, hashed_password FROM users"""
                curs.execute(sql)
                for row in curs.fetchall():
                    loaded_user = User()
                    loaded_user.__id = row.get('id')
                    loaded_user.username = row.get('username')
                    loaded_user.email = row.get('email')
                    loaded_user._User__hashed_password = row.get('hashed_password')
                    rv.append(loaded_user)
        return rv

    def delete(self):
        with psycopg2.connect(DB_COMPLETE_URI) as db_con:
            with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                sql = """DELETE FROM Users WHERE id=%s"""
                curs.execute(sql, (self.__id,))
                self._User__id = -1
                return True


if __name__ == '__main__':
    import os
    DB_NAME = "msgs_server"
    DB_URI = os.environ.get('SERVER_DB_URI')  # postgresql://postgres@localhost
    DB_COMPLETE_URI = "/".join([DB_URI, DB_NAME])

    x = User()
    x.username = "Test username"
    x.email = "Test email"
    x.hashed_password = "password1"
    print(x.check_password("password2", x.hashed_password))
    print(x.check_password("password1", x.hashed_password))
    x.set_new_password("password1", x.hashed_password, "password2", "password2")
    print(x.check_password("password2", x.hashed_password))
    print(x.check_password("password1", x.hashed_password))
    print(len(x.hashed_password))
    print(x.hashed_password)
    # x.save_to_db()
    y = x.load_user_by_id(14)
    print(y)
    print(y.check_password("password2", y.hashed_password))
    print(x.load_all_users())
    y.username = "Test username changed"
    y.save_to_db()
    print(x.load_all_users())
    y.delete()
    print(x.load_all_users())
    print(y.id)

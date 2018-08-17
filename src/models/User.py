import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
# from . import DB_COMPLETE_URI


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
        else:
            print("Wrong password or new password do not match")

    def save_to_db(self):
        if self.__id == -1:
            with psycopg2.connect(DB_COMPLETE_URI) as db_con:
                with db_con.cursor(cursor_factory=RealDictCursor) as curs:
                    sql = """INSERT INTO Users(username, email, hashed_password) VALUES(%s, %s, %s) RETURNING id"""
                    values = (self.username, self.email, self.hashed_password)
                    curs.execute(sql, values)
                    self.__id = curs.fetchone().get('id')
            return True
        return False


if __name__ == '__main__':
    x = User()
    x.hashed_password = "password1"
    print(x.check_password("password2", x.hashed_password))
    print(x.check_password("password1", x.hashed_password))
    x.set_new_password("password1", x.hashed_password, "password2", "password2")
    print(x.check_password("password2", x.hashed_password))
    print(x.check_password("password1", x.hashed_password))
    print(len(x.hashed_password))
    print(x.hashed_password)

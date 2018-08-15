import psycopg2
import bcrypt


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
        self.__hashed_password = User.password_hash(password)

    @staticmethod
    def password_hash(password):
        return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

    def verify_password(self, password):
        return self.check_password(password, self.hashed_password)

    @staticmethod
    def check_password(password, hashed):
        return bcrypt.checkpw(bytes(password, 'utf-8'), hashed)


if __name__ == '__main__':
    x = User()
    x.hashed_password = "pass1"
    print(x.verify_password("pass2"))
    print(x.verify_password("pass1"))

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
    def set_password(self, password):
        self.__hashed_password = User.password_hash(password)

    @staticmethod
    def password_hash(password):
        return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_password(password, hashed):
        return bcrypt.checkpw(bytes(password, 'utf-8'), hashed)


if __name__ == '__main__':
    hashed = User.password_hash('test_pass123')
    print(hashed)
    print(User.check_password('test_pass123', hashed))
    print(User.check_password('test_pass1231', hashed))
    print(User.check_password('test_pass123', hashed))

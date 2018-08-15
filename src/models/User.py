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
        if len(password) >= 8:
            self.__hashed_password = User.password_hash(password)
        else:
            print("Password to short. Minimum length is 8 characters.")

    @staticmethod
    def password_hash(password):
        return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_password(password, hashed):
        return bcrypt.checkpw(bytes(password, 'utf-8'), hashed)

    def check_user_password(self, password):
        return self.check_password(password, self.hashed_password) if self.hashed_password else None

    def set_new_password(self, old_pass, new_pass, new_pass_confirm):
        if self.check_user_password(old_pass) and new_pass == new_pass_confirm:
            self.hashed_password = new_pass
        else:
            print("Wrong password or new password do not match")


if __name__ == '__main__':
    x = User()
    x.hashed_password = "password1"
    print(x.check_user_password("password2"))
    print(x.check_user_password("password1"))
    x.set_new_password("password1", "password2", "password2")
    print(x.check_user_password("password2"))
    print(x.check_user_password("password1"))

import json
import os


class User:
    def __init__(self, username=None, password=None):
        self.d = {
            'username': username,
            'password': password,
        }

    @property
    def username(self):
        return self.d['username']

    @property
    def password(self):
        return self.d['password']

    @staticmethod
    def fromJson(f):
        d = json.load(f)
        u = User()
        u.d.update(d)
        return u

    def toJson(self, f):
        json.dump(self.d, f)


class UserManager:
    def __init__(self):
        USERPATH = './user.json'
        if not os.path.exists(USERPATH):
            print('首次使用时需输入用户名和密码：（如需重新输入请删除当前目录下的user.json文件）')
            with open(USERPATH, 'w', encoding='utf8') as f:
                username = input('用户名：')
                password = input('密码：')
                User(username, password).toJson(f)

        with open(USERPATH, 'r', encoding='utf8') as f:
            self.user = User.fromJson(f)

    def getUser(self):
        return self.user.username, self.user.password

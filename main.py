import os
import requests as r

# from cqu_auth import CquAuth
from auth import login
from userProfile import UserManager

from myconfig import ConfigReport

USE_PROXIES = False  # TODO
proxies = None
if USE_PROXIES:
   proxies = {
      'http': 'http://127.0.0.1:9999',
      'https': 'http://127.0.0.1:9999',
   }

print("本脚本会基于上次打卡记录构造本次打卡数据，并自动提交。")

# 首次使用时输入用户名密码
username, password = UserManager().getUser()

print('登录中...')
# cquauth = CquAuth(username, password, proxies=proxies)
# s = cquauth.login()
s = r.Session()
login(s, username, password)

try:
   ConfigReport().default_method(s, proxies=proxies)
   print('打卡成功！')
except Exception as e:
   print('错误！\n', e)

os.system('pause')


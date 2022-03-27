使用了 [CQU_Authenticator库](https://github.com/barryZZJ/CQU_Authenticator) 用于认证。

# 使用
注意：首次执行时需要输入用户名和密码，并保存在`user.json`中，以后不需要再输入。删除该文件后可以重新输入用户名和密码。
## 使用可执行文件运行
[下载可执行文件]()后，双击运行即可。

## 使用Python运行脚本
1. 安装环境
```
pip install requests
pip install beautifulsoup4
pip install pycryptodome
```
2. 运行`main.py`即可


# 执行过程说明
|host|url|方法|获得的内容|
|---|---|---|---|
|i.cqu.edu.cn|/qljfwapp4/sys/lwStuReportEpidemic/*default/index.do|GET|APPNAME、APPID|
|i.cqu.edu.cn|/qljfwapp4/sys/lwpub/mobile/api/authenticated/funauth/users/roles.do|POST|ROLEID|
|i.cqu.edu.cn|/qljfwapp4/sys/lwpub/mobile/api/authenticated/users/setupRole.do|POST|_WEU (cookie)|



# 简介

本脚本会自动复制昨天的打卡记录，修改日期等信息后作为今天的打卡记录提交，如有关键信息变动，请手动打卡。

# 使用
注意：首次执行时需要输入统一身份认证登录用户名和密码，并保存在`user.json`中，以后不需要再输入。删除该文件后可以重新输入用户名和密码。
## 可执行文件
在 [release](https://github.com/barryZZJ/CQU_crona_auto_report/releases) 页面下载CronaAutoReport.exe后，双击运行即可。

## 用Python运行脚本
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


# Changelog

`v2.0`: 适配了新版统一身份认证系统，感谢 https://github.com/Hagb/pymycqu/tree/dev

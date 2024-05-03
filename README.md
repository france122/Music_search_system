# 歌词检索系统
  
## 系统功能介绍
登录界面：用户名：admin ； 密码：123456

主题抽取、情感分析 

## 依赖项
本系统基于Html+Flask+Mysql框架，需要安装以下的python包
- Flask(backend)
- Pymysql(connecting the backend and the database)

## 运行方法
- 在navicat运行全部的sql文件，修改data.py中有关db的username和password;
- 在编辑配置中新建编辑器如Flask Server，选择路径为app.py文件，
- 运行得到网站的url，点击url即可在浏览器中登录该歌词系统

```bash
pip install *

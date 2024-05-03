import calendar
from datetime import datetime
from flask import Flask, render_template, redirect, request
import musicdata as mud
import functions as func

app = Flask(__name__, static_url_path="/")
app.secret_key = 'ahdbahibaiuhjonbawiuh'


# 设置默认界面
@app.route("/")
def default_page():
    return redirect('/login')


# 主界面接口
@app.route('/index')
def main_interface():
    return render_template("index.html")


# 添加歌曲信息
@app.route('/add-songs-data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'GET':
        return render_template('add-songs-data.html')
    if request.method == 'POST':
        func.add_data()
        return redirect('/songs-datas')

# 登录接口
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        res = func.login()
        if res == 1:
            return redirect('/index')
        else:
            return '账号不为admin,或密码错误！'


if __name__ == '__main__':
    app.run(port=8000)

from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request

import model.search
from model.check_login import is_existed,exist_user,is_null
from model.check_regist import add_user
from model.search import search_results
from model.sql_query import sql_query
from musicdata import db

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('user_login'))

@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method=='POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('login.html', message=login_massage)
        elif is_existed(username, password):
            return render_template('index.html', username=username)
        elif exist_user(username):
            login_massage = "温馨提示：密码错、。误，请输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_massage)
    return render_template('login.html')

@app.route("/regiser",methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username,password):
            login_massage = "温馨提示：账号和密码是必填"
            return render_template('register.html', message=login_massage)
        elif exist_user(username):
            login_massage = "温馨提示：用户已存在，请直接登录"
            # return redirect(url_for('user_login'))
            return render_template('register.html', message=login_massage)
        else:
            add_user(request.form['username'], request.form['password'] )
            return render_template('index.html', username=username)
    return render_template('register.html')


@app.route("/index", methods=["POST", "GET"])
def search():
    if request.args.get('key_word', None) == None:  # 如果没有检测到关键字提交，就停留在检索页面
        print("未传参")
        return render_template("search.html")  # 映射到检索页面
    else:  # 如果有关键词提交
        key_words = request.args.get('key_word')  # 将传来的关键词赋给key_word
        search_results = model.search.search_results(key_words)  # 在表里查询符合条件的条目赋给key_words

        return render_template("results.html", search_results = search_results)  # 映射到结果的页面，并将查询到的条目传过去


if __name__ == '__main__':
    #server = pywsgi.WSGIServer(('127.0.0.1', 8000), app)
    #server.serve_forever()
    app.run(debug=True,host='0.0.0.0',port = 6688)

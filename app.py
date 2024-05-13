from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request

import model.search
from model.check_login import is_existed,exist_user,is_null
from model.check_regist import add_user
from model.search import songsearch_results
from model.sql_query import sql_query
from model.search import artistsearch_results
from model.search import sql_artistquery
from model.search import albumsearch_results
from model.search import sql_albumquery
from model.whoosh_test import whoosh_search,whoosh_index
from musicdata import db
from model.Jieba_query import inverted_index
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
            return render_template('search.html', username=username)
        elif exist_user(username):
            login_massage = "温馨提示：密码错误，请输入正确密码"
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
            return render_template('search.html', username=username)
    return render_template('register.html')


@app.route("/lyrics_search", methods=["GET","POST"])
def lyrics_search():
    if request.args.get('key_word', None) == None:  # 如果没有检测到关键字提交，就停留在检索页面
        print("未传参")
        return render_template("search.html")  # 映射到检索页面
    else:  # 如果有关键词提交
        key_words = request.args.get('key_word')  # 将传来的关键词赋给key_word
        keywords = key_words.split()
        search_results1 = model.Jieba_query.show_results(keywords, inverted_index)  # 在表里查询符合条件的条目赋给key_words
        whoosh_index()
        search_results2 = whoosh_search(keywords)
        return render_template("results.html", search_results1=search_results1,search_results2=search_results2)  # 映射到结果的页面，并将查询到的条目传过去

@app.route("/search", methods=["GET"])
def search():
    search_params = {}
    if request.args.get('key_artist'):
        search_params['artist'] = request.args.get('key_artist').strip()
    if request.args.get('key_song'):
        search_params['song'] = request.args.get('key_song').strip()
    if request.args.get('key_album'):
        search_params['album'] = request.args.get('key_album').strip()
    if request.args.get('key_version'):
        search_params['version'] = request.args.get('key_version').strip()
    if not search_params:
        return render_template("search.html", error="请至少填写一个搜索条件。")

    # 初始结果集为空列表
    results_sets = []
    if 'artist' in search_params:
        artist_results = set(model.search.artistsearch_results(search_params['artist']))
        results_sets.append(artist_results)
    if 'song' in search_params:
        song_results = set(model.search.songsearch_results(search_params['song']))
        results_sets.append(song_results)
    if 'album' in search_params:
        album_results = set(model.search.albumsearch_results(search_params['album']))
        results_sets.append(album_results)
    if 'version' in search_params:
        version_results = set(model.search.versionsearch_results(search_params['version']))
        results_sets.append(version_results)

    # 取交集
    final_results = set.intersection(*results_sets) if results_sets else []

    return render_template("results.html", search_results=list(final_results))

if __name__ == '__main__':
    #server = pywsgi.WSGIServer(('127.0.0.1', 8000), app)
    #server.serve_forever()
    app.run(debug=True,host='0.0.0.0',port = 6688)
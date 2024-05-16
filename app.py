from flask import Flask, render_template, redirect, url_for, request
import model.search
from model.check_login import is_existed, exist_user, is_null
from model.check_regist import add_user
from model.search import songsearch_results, artistsearch_results, albumsearch_results, versionsearch_results, get_song_details, get_song_detail_by_id, get_artist_biography
from musicdata import db
from model.Jieba_query import inverted_index

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('user_login'))

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_message = "温馨提示：账号和密码是必填"
            return render_template('login.html', message=login_message)
        elif is_existed(username, password):
            return render_template('search.html', username=username)
        elif exist_user(username):
            login_message = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_message)
        else:
            login_message = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_message)
    return render_template('login.html')

@app.route("/register", methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_message = "温馨提示：账号和密码是必填"
            return render_template('register.html', message=login_message)
        elif exist_user(username):
            login_message = "温馨提示：用户已存在，请直接登录"
            return render_template('register.html', message=login_message)
        else:
            add_user(request.form['username'], request.form['password'])
            return render_template('search.html', username=username)
    return render_template('register.html')

from flask import Flask, render_template, redirect, url_for, request
import model.search
from model.check_login import is_existed, exist_user, is_null
from model.check_regist import add_user
from model.search import songsearch_results, artistsearch_results, albumsearch_results, versionsearch_results, get_song_details, get_song_detail_by_id, get_artist_biography
from musicdata import db
from model.Jieba_query import inverted_index

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('user_login'))

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_message = "温馨提示：账号和密码是必填"
            return render_template('login.html', message=login_message)
        elif is_existed(username, password):
            return render_template('search.html', username=username)
        elif exist_user(username):
            login_message = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_message)
        else:
            login_message = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_message)
    return render_template('login.html')

@app.route("/register", methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_message = "温馨提示：账号和密码是必填"
            return render_template('register.html', message=login_message)
        elif exist_user(username):
            login_message = "温馨提示：用户已存在，请直接登录"
            return render_template('register.html', message=login_message)
        else:
            add_user(request.form['username'], request.form['password'])
            return render_template('search.html', username=username)
    return render_template('register.html')

@app.route("/search", methods=["GET", "POST"])
def search():
    search_params = {}
    artist_biography = None
    major_artists = ['苏打绿', '凤凰传奇', '周杰伦', '李宇春', '张学友', '五月天']

    if request.args.getlist('key_word'):
        search_params['words'] = request.args.getlist('key_word')
    if request.args.get('key_artist'):
        search_params['artist'] = request.args.get('key_artist').strip()
        if search_params['artist'] in major_artists:
            artist_biography = get_artist_biography(search_params['artist'])
    if request.args.get('key_song'):
        search_params['song'] = request.args.get('key_song').strip()
    if request.args.get('key_album'):
        search_params['album'] = request.args.get('key_album').strip()
    if request.args.get('key_version'):
        search_params['version'] = request.args.get('key_version').strip()

    if not search_params:
        return render_template("search.html", error="请至少填写一个搜索条件。")

    results_sets = []

    if 'words' in search_params and search_params['words']:
        word_results_sets = []
        for keyword in search_params['words']:
            if keyword.strip():  # 只处理非空关键词
                search_results = model.Jieba_query.show_results(keyword.split(), inverted_index)
                word_results_sets.append(set(search_results))
        if word_results_sets:
            combined_word_results = set.intersection(*word_results_sets)
            if combined_word_results:  # 只添加非空集合
                results_sets.append(combined_word_results)

    if 'artist' in search_params and search_params['artist']:
        artist_results = set(artistsearch_results(search_params['artist']))
        if artist_results:  # 只添加非空集合
            results_sets.append(artist_results)
    if 'song' in search_params and search_params['song']:
        song_results = set(songsearch_results(search_params['song']))
        if song_results:  # 只添加非空集合
            results_sets.append(song_results)
    if 'album' in search_params and search_params['album']:
        album_results = set(albumsearch_results(search_params['album']))
        if album_results:  # 只添加非空集合
            results_sets.append(album_results)
    if 'version' in search_params and search_params['version']:
        version_results = set(versionsearch_results(search_params['version']))
        if version_results:  # 只添加非空集合
            results_sets.append(version_results)

    # 如果有多个条件，取交集；否则直接使用单个条件的结果
    if results_sets:
        final_results = results_sets[0]
        for result_set in results_sets[1:]:
            final_results &= result_set
    else:
        final_results = set()

    # 从后端获取详细的歌曲信息
    detailed_results = get_song_details(final_results)

    # 调试输出
    print("Search Parameters:", search_params)
    print("Final Results:", final_results)
    print("Detailed Results:", detailed_results)

    return render_template("results.html", search_results=detailed_results, artist_biography=artist_biography)

@app.route("/song_detail/<song_id>")
def song_detail(song_id):
    song_detail = get_song_detail_by_id(song_id)
    if not song_detail:
        return render_template("songdetail.html", error="找不到该歌曲的详细信息。")
    return render_template("songdetail.html", song_detail=song_detail)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6688)

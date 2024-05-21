from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import model.search
from model.check_login import is_existed, exist_user, is_null
from model.check_regist import add_user
from model.search import (songsearch_results, emotionsearch_results, artistsearch_results,
                          albumsearch_results, versionsearch_results, get_song_details,
                          get_song_detail_by_id, get_artist_biography)
import time
from musicdata import db, cursor
from model.whoosh_test import whoosh_search
from model.Jieba_query import inverted_index

app = Flask(__name__)
app.secret_key = '1234'

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
            session['username'] = username
            return redirect(url_for('index1'))
        elif exist_user(username):
            login_message = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_message)
        else:
            login_message = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_message)
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
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
            add_user(username, password)
            return redirect(url_for('index1'))
    return render_template('register.html')

@app.route('/test_search', methods=['GET', 'POST'])
def test_search():
    key_word = request.args.get('key_word')  # 从GET请求中获取key_word
    key_word = key_word.split()
    search_results1, search_results2, time1, time2 = lyrics_search(key_word)
    return render_template('compare.html', search_results1=search_results1, search_results2=search_results2, time1=time1, time2=time2)

def lyrics_search(keywords):
    start_time1 = time.time()
    search_results1 = model.Jieba_query.show_results(keywords, inverted_index)
    end_time1 = time.time()
    time1 = round(end_time1 - start_time1, 3)
    start_time2 = time.time()
    search_results2 = whoosh_search(keywords)
    end_time2 = time.time()
    time2 = round(end_time2 - start_time2, 3)
    detailed_results1 = get_song_details(search_results1)
    detailed_results2 = get_song_details(search_results2)
    return detailed_results1, detailed_results2, time1, time2

@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route("/search", methods=["POST"])
def search():
    search_params = {}
    artist_biography = None
    major_artists = ['苏打绿', '凤凰传奇', '周杰伦', '李宇春', '张学友', '五月天']

    # 获取搜索参数
    fields = request.form.getlist('fields[]')
    for field in fields:
        if field and request.form.get(field):
            search_params[field] = request.form.get(field).strip()
            if field == 'key_artist' and search_params[field] in major_artists:
                artist_biography = get_artist_biography(search_params[field])

    arousal = request.form.get('arousal')
    valence = request.form.get('valence')

    if not search_params and (arousal is None or valence is None):
        return render_template("index.html", error="请至少填写一个搜索条件。")

    results_sets = []

    # 全字段搜索
    if 'key_all' in search_params and search_params['key_all']:
        all_results = all_field_search_results(search_params['key_all'])
        if all_results:
            results_sets.append(all_results)

    # 处理各个字段的搜索
    for field, value in search_params.items():
        if field == 'key_word':
            word_results_sets = []
            for keyword in value.split():
                if keyword.strip():  # 只处理非空关键词
                    search_results = model.Jieba_query.show_results(keyword.split(), inverted_index)
                    word_results_sets.append(set(search_results))
            if word_results_sets:
                combined_word_results = set.union(*word_results_sets)
                if combined_word_results:  # 只添加非空集合
                    results_sets.append(combined_word_results)
        elif field == 'key_artist':
            artist_results = set(artistsearch_results(value))
            if artist_results:  # 只添加非空集合
                results_sets.append(artist_results)
        elif field == 'key_song':
            song_results = set(songsearch_results(value))
            if song_results:  # 只添加非空集合
                results_sets.append(song_results)
        elif field == 'key_album':
            album_results = set(albumsearch_results(value))
            if album_results:  # 只添加非空集合
                results_sets.append(album_results)
        elif field == 'key_version':
            version_results = set(versionsearch_results(value))
            if version_results:  # 只添加非空集合
                results_sets.append(version_results)

    # 取交集
    if results_sets:
        final_results = results_sets[0]
        for result_set in results_sets[1:]:
            final_results &= result_set
    else:
        final_results = set()

    # 添加情感搜索逻辑
    if arousal and valence:
        if final_results:
            # 如果有其他检索条件的结果，对这些结果进行情感排序
            final_results = emotionsearch_results(arousal, valence, list(final_results))
        else:
            # 如果没有其他检索条件的结果，进行全表情感搜索
            final_results = emotionsearch_results(arousal, valence)
    else:
        if not final_results:
            # 如果没有情感参数且没有其他条件的结果，返回空结果
            return render_template("index.html", error="没有符合条件的结果。")

    # 从后端获取详细的歌曲信息
    detailed_results = get_song_details(final_results)

    # 使用 session 存储搜索结果
    session['detailed_results'] = detailed_results
    session['artist_biography'] = artist_biography

    return redirect(url_for('results'))

@app.route('/results')
def results():
    detailed_results = session.get('detailed_results', [])
    artist_biography = session.get('artist_biography', None)
    return render_template("results.html", search_results=detailed_results, artist_biography=artist_biography)

def all_field_search_results(keyword):
    # 对各个字段分别进行搜索并转换为集合
    word_results = set(model.Jieba_query.show_results(keyword.split(), inverted_index))
    artist_results = set(artistsearch_results(keyword))
    song_results = set(songsearch_results(keyword))
    album_results = set(albumsearch_results(keyword))
    version_results = set(versionsearch_results(keyword))

    # 确保每个结果集是单列，并去重
    def extract_single_column(results):
        return set(item[0] for item in results if isinstance(item, (list, tuple)) and len(item) > 0)

    word_results = extract_single_column(word_results)
    artist_results = extract_single_column(artist_results)
    song_results = extract_single_column(song_results)
    album_results = extract_single_column(album_results)
    version_results = extract_single_column(version_results)

    # 将结果取并集并去重
    all_results = word_results | artist_results | song_results | album_results | version_results

    return all_results

@app.route("/song_detail/<song_id>")
def song_detail(song_id):
    song_detail = get_song_detail_by_id(song_id)
    if not song_detail:
        return render_template("songdetail.html", error="找不到该歌曲的详细信息。")
    return render_template("songdetail.html", song_detail=song_detail)

@app.route('/index1')
def index1():
    username = session["username"]
    return render_template('index.html', username=username)

@app.route("/self")
def self():
    myusername = session['username']
    sql = "select SongID from collects where username = 'admin'"
    cursor.execute(sql)
    collect_results = []
    collect_results_songID = cursor.fetchall()
    collect_results = get_song_details(collect_results_songID)
    return render_template("self.html", collect_results=collect_results)

@app.route('/add_to_favorites/<song_id>', methods=['POST'])
def add_to_favorites(song_id):
    username = session['username']
    if not username:
        return jsonify({'message': 'Username is required'}), 400
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO collects (username, SongID) VALUES (%s, %s)"
            cursor.execute(sql, (username, song_id))
        db.commit()  # 假设 db 是你的数据库连接对象
    except Exception as e:
        db.rollback()
        return jsonify({'message': 'Failed to add song to collects: ' + str(e)}), 500
    return jsonify({'message': 'Song added to collects'})

@app.route('/remove_from_favorites/<song_id>', methods=['POST'])
def remove_from_favorites(song_id):
    username = session['username']
    if not username:
        return jsonify({'message': 'Username is required'}), 400
    try:
        with db.cursor() as cursor:
            sql = "DELETE FROM collects WHERE username=%s AND SongID = %s"
            cursor.execute(sql, (username, song_id))

        db.commit()  # 假设 db 是你的数据库连接对象
    except Exception as e:
        db.rollback()
        return jsonify({'message': 'Failed to remove song from collects: ' + str(e)}), 500
    return jsonify({'message': 'Song has been removed from collects'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6688)

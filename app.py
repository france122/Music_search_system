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

    # 获取搜索参数
    fields = request.args.getlist('fields[]')
    for field in fields:
        if field and request.args.get(field):
            search_params[field] = request.args.get(field).strip()
            if field == 'key_artist' and search_params[field] in major_artists:
                artist_biography = get_artist_biography(search_params[field])

    if not search_params:
        return render_template("search.html", error="请至少填写一个搜索条件。")

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

    # 从后端获取详细的歌曲信息
    detailed_results = get_song_details(final_results)

    # 调试输出
    print("Search Parameters:", search_params)
    print("Final Results:", final_results)
    print("Detailed Results:", detailed_results)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6688)

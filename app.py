from flask import Flask, render_template, redirect, url_for, request, jsonify, session,send_file
import model.search
import jieba
from model.check_login import is_existed, exist_user, is_null
from model.check_regist import add_user
from model.search import (songsearch_results, emotionsearch_results, artistsearch_results,
                          albumsearch_results, versionsearch_results, get_song_details,
                          get_song_detail_by_id, get_artist_biography)
import time
import os
from musicdata import db, cursor
from model.whoosh_test import whoosh_search
from model.Jieba_query import inverted_index
from model.search_similarmeasurement import show_results_similarity
app = Flask(__name__)
app.secret_key = '1234'
import pandas as pd
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
    raw_key_words = request.args.get('key_words')  # 从GET请求中获取key_word
    key_words = raw_key_words.split()
    search_words=[]
    for key_word in key_words:
        seg_list = jieba.lcut_for_search(key_word)
        search_words.extend(seg_list)
    search_results1, search_results2, time1, time2 = lyrics_search(search_words)
    length1,length2=len(search_results1),len(search_results2)
    if length1>30:
        search_results1=search_results1[:30]
        length1=30
    if length2>30:
        search_results2=search_results2[:30]
        length2=30

    start_time3 = time.time()
    (search_results3,similar_scores_and_highlights) = model.search_similarmeasurement.show_results_similarity(raw_key_words)
    end_time3 = time.time()
    time3 = round(end_time3 - start_time3, 3)
    detailed_results3 = get_song_details(search_results3)
    return render_template('compare.html', search_results1=search_results1, search_results2=search_results2,search_results3=detailed_results3,results_detail_similarity=similar_scores_and_highlights, time1=time1, time2=time2,time3=time3,search_results1_len=length1,search_results2_len=length2,search_results3_len=len(search_results3))

def lyrics_search(keywords):
    start_time1 = time.time()
    (search_results1,tfidf_scores) = model.Jieba_query.show_results(keywords, inverted_index)
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

@app.route("/search", methods=["GET", "POST"])
def search():

    if request.method == "POST":
        print(request.form)  # 打印表单提交的数据

        refine_query = request.form.get('secondary_search_query')
        previous_song_ids = request.form.getlist('previous_song_ids')  # 获取之前的搜索结果

        if refine_query:
            # 二次检索逻辑
            print(f"Refine query: {refine_query}")

            if not previous_song_ids:
                return render_template("results.html", error="没有之前的搜索结果。", search_results=[])

            previous_song_ids = set(previous_song_ids)
            print(f"Previous song IDs: {previous_song_ids}")

            (all_results,tfidf_scores,similar_scores)= all_field_search_results(refine_query)
            print(f"All results for refine query '{refine_query}': {all_results}")

            if not all_results:
                return render_template("results.html", error="没有符合条件的结果。", search_results=[])

            refined_song_ids = previous_song_ids & set(all_results)
            print(f"Refined song IDs after intersection: {refined_song_ids}")

            if not refined_song_ids:
                return render_template("results.html", error="没有符合条件的结果。", search_results=[])

            song_ids = [(song_id,) for song_id in refined_song_ids]
            search_results_len = len(refined_song_ids)
            print(f"Song IDs for get_song_details: {song_ids}")
            detailed_results = get_song_details(song_ids)
            print(f"Detailed results: {detailed_results}")

            return render_template("results.html", search_results=detailed_results, previous_song_ids=list(refined_song_ids),search_results_len = search_results_len)

        # 初次检索逻辑
        search_params = {}

        artist_biography = None
        major_artists = ['苏打绿', '凤凰传奇', '周杰伦', '李宇春', '张学友', '五月天']

        fields = request.form.getlist('fields[]')
        for field in fields:
            if field and request.form.get(field):
                search_params[field] = request.form.get(field).strip()
                if field == 'key_artist' and search_params[field] in major_artists:
                    print(f"Searching for major artist: {search_params[field]}")
                    artist_biography = get_artist_biography(search_params[field])
                    print(f"Artist biography: {artist_biography}")

        arousal = request.form.get('arousal')
        valence = request.form.get('valence')

        if not search_params and (arousal is None or valence is None):
            return render_template("index.html", error="请至少填写一个搜索条件。")

        results_sets = []
        tfidf_scores = []
        similar_scores_and_highlights = []
        if 'key_all' in search_params and search_params['key_all']:
            (all_results,tfidf_scores,similar_scores_and_highlights ) = all_field_search_results(search_params['key_all'])
            if all_results:
                results_sets.append(set(all_results))

        for field, value in search_params.items():
            if field == 'key_word':
                word_results_sets = []
                for keyword in value.split():
                    if keyword.strip():
                        if len(keyword) <= 4:

                            seg_list = jieba.lcut_for_search(keyword)
                            (search_results,tfidf_scores) = model.Jieba_query.show_results(seg_list, inverted_index)
                            word_results_sets.append(set(result[0] for result in search_results))
                        else:
                            (search_results,similar_scores_and_highlights) = model.search_similarmeasurement.show_results_similarity(keyword)
                            word_results_sets.append(set(result[0] for result in search_results))
                if word_results_sets:
                    lyrics_yesorno = 1
                    combined_word_results = set.union(*word_results_sets)
                    if combined_word_results:
                        results_sets.append(combined_word_results)

            elif field == 'key_artist':
                artist_results = set(result[0] for result in artistsearch_results(value))
                if artist_results:
                    results_sets.append(artist_results)
            elif field == 'key_song':
                song_results = set(result[0] for result in songsearch_results(value))
                if song_results:
                    results_sets.append(song_results)
            elif field == 'key_album':
                album_results = set(result[0] for result in albumsearch_results(value))
                if album_results:
                    results_sets.append(album_results)
            elif field == 'key_version':
                version_results = set(result[0] for result in versionsearch_results(value))
                if version_results:
                    results_sets.append(version_results)
            #elif field == 'key_lyrics':
            #    lyrics_results = lyrics_search_results(value)
            #    if lyrics_results:
            #        results_sets.append(set(result[0] for result in lyrics_results))
        if results_sets:
            final_results = results_sets[0]
            for result_set in results_sets[1:]:
                final_results &= result_set
        else:
            final_results = set()

        print(f"Final search results: {final_results}")
        print(f"Number of final search results: {len(final_results)}")

        if arousal and valence:
            if final_results:
                final_results = emotionsearch_results(arousal, valence, list(final_results))
            else:
                final_results = emotionsearch_results(arousal, valence)
        else:
            if 'key_word' in search_params or 'key_all' in search_params:
                if final_results:
                    songid_pd = pd.DataFrame(final_results,columns=['SongID'])
                    tfidf_scores_pd = pd.DataFrame(tfidf_scores,columns=['SongID','Tfidf'])
                    similar_scores_and_pd = pd.DataFrame(similar_scores_and_highlights,columns=['SongID','Lyrics','Similar'])
                    score_prepare = pd.merge(songid_pd,tfidf_scores_pd,on="SongID",how="outer")
                    score = pd.merge(score_prepare, similar_scores_and_pd,on="SongID",how="outer")
                    score.fillna(value=10,inplace=True)
                    #print(score['Tfidf'])
                    score['Score'] = score['Tfidf'] + score['Similar']
                    score_sorted = score.sort_values(by='Score',ascending=False)
                    score_sorted = score_sorted.reset_index(drop=True)
                    print(score_sorted)
                    #print("******************",type(myfinal_results))
                    myfinal_results = []
                    for i in range(min(score_sorted.shape[0],20)):
                        #print("*****",score_sorted.size)
                        songid = score_sorted.loc[i, 'SongID']
                        #print(i, score_sorted.shape[0], songid, score_sorted.loc[i, 'Score'])

                        if songid in final_results:
                            myfinal_results.append(songid)

                    final_results = myfinal_results
                elif not final_results:
                    return render_template("index.html", error="没有符合条件的结果。")



        detailed_results = []
        for song_id in final_results:
            song_ids = [(song_id,)]
            detailed_results = detailed_results + get_song_details(song_ids)
        #print("++++++++++++",detailed_results[0])

        print(f"Detailed results: {detailed_results}")
        print(f"Number of detailed results: {len(detailed_results)}")
        search_results_len = len(final_results)
        return render_template("results.html", search_results=detailed_results, previous_song_ids=list(final_results),search_results_len = search_results_len)

    elif request.method == "GET":
        artist = request.args.get('key_artist')
        if not artist:
            return render_template("index.html", error="未指定歌手。")

        artist_biography = get_artist_biography(artist)
        print(f"GET request for artist biography: {artist_biography}")

        results_sets = set(result[0] for result in artistsearch_results(artist))

        if not results_sets:
            return render_template("index.html", error="没有符合条件的结果。")

        song_ids = [(song_id,) for song_id in results_sets]
        detailed_results = get_song_details(song_ids)
        search_results_len = len(results_sets)
        return render_template("results.html", search_results=detailed_results, artist_biography=artist_biography, previous_song_ids=list(results_sets),search_results_len = search_results_len)

def all_field_search_results(keyword):
    word_results_1 = []
    word_results_2 = []
    tfidf_scores = []
    similar_scores_and_highlights = []
    for keyword_01 in keyword.split():
        #print("___________________", len(keyword_01))
        if len(keyword_01) <= 4:
            seg_list = jieba.lcut_for_search(keyword_01)
            (result1,tfidf_scores) = model.Jieba_query.show_results(seg_list, inverted_index)
            for result in result1:
                word_results_1.append(result[0])
                # print("___________", result[0])
        else:
            (similar_results, similar_scores_and_highlights) = model.search_similarmeasurement.show_results_similarity(keyword)
            for result in similar_results:
                word_results_2.append(result[0])
                # print("_____", result[0])
    word_results = set(word_results_1) | set(word_results_2)
    #word_results = set(result[0] for result in model.Jieba_query.show_results(keyword.split(), inverted_index))
    artist_results = set(result[0] for result in artistsearch_results(keyword))
    song_results = set(result[0] for result in songsearch_results(keyword))
    album_results = set(result[0] for result in albumsearch_results(keyword))
    version_results = set(result[0] for result in versionsearch_results(keyword))

    all_results = word_results | artist_results | song_results | album_results | version_results
    print(f"All field search results for '{keyword}': {all_results}")

    return all_results,tfidf_scores,similar_scores_and_highlights

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

# @app.route('/add_to_favorites/<song_id>', methods=['POST'])
# def add_to_favorites(song_id):
#     username = session['username']
#     if not username:
#         return jsonify({'message': 'Username is required'}), 400
#     try:
#         with db.cursor() as cursor:
#             sql = "INSERT INTO collects (username, SongID) VALUES (%s, %s)"
#             cursor.execute(sql, (username, song_id))
#         db.commit()  # 假设 db 是你的数据库连接对象
#     except Exception as e:
#         db.rollback()
#         return jsonify({'message': 'Failed to add song to collects: ' + str(e)}), 500
#     return jsonify({'message': 'Song added to collects'})

@app.route('/add_to_favorites/<song_id>', methods=['POST'])
def add_to_favorites(song_id):
    username = session['username']
    if not username:
        return jsonify({'message': '需要用户名'}), 400
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO collects (username, SongID) VALUES (%s, %s)"
            cursor.execute(sql, (username, song_id))
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({'message': '添加歌曲到收藏失败: ' + str(e)}), 500
    return '', 204  # 无内容状态码

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
    return '', 204  # 无内容状态码

@app.route('/audio/<song_id>')
def get_audio(song_id):
    audio_file_path = os.path.join(app.root_path, 'static/source/mp3', f'{song_id}.mp3')
    if os.path.exists(audio_file_path):
        return send_file(audio_file_path)
    else:
        return "Audio file not found", 404

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=6688)
import requests
import json
import pymysql

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'usedname',
    'password': 'password',
    'db': 'music',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 百度API情感分析相关配置
token = "Yourtoken"  # 请替换为你的真实assess_token
url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={}'.format(token)

analyzed_songs = {}


def get_emotion(songname, lyrics):
    # 检查歌曲是否已经分析过
    if songname in analyzed_songs:
        return analyzed_songs[songname]

    headers = {'Content-Type': 'application/json'}
    new_each = {'text': lyrics}
    response = requests.post(url, json=new_each, headers=headers)
    if response.status_code == 200:
        res_json = response.json()
        if 'items' in res_json and res_json['items']:
            item = res_json['items'][0]
            negative = item['negative_prob']
            positive = item['positive_prob']
            if positive>negative:
                emotion = "positive"
            elif  positive<negative:
                emotion="negative"
            else:
                emotion="neutral"

        else:
            emotion= "neutral"
    else:
        emotion= "error"

    # 缓存结果
    analyzed_songs[songname] = emotion
    return emotion


def update_songs_emotion(conn, song_id, songname, emotion):
    with conn.cursor() as cursor:
        sql = "UPDATE songs SET emotion = %s WHERE SongID = %s"
        cursor.execute(sql, (emotion, song_id))
    conn.commit()


def main():
    # 连接数据库
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:

            sql = "SELECT SongID, SongName, lyrics FROM songs "
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                song_id = row['SongID']
                songname = row['SongName']
                lyrics = row['lyrics']
                emotion = get_emotion(songname, lyrics)
                if emotion != "error":  # 忽略API调用错误
                    update_songs_emotion(connection, song_id, songname, emotion)
                    print(f"Lyrics ID: {song_id}, Emotion: {emotion}")
                else:
                    print(f"Error analyzing lyrics for song '{songname}' (ID: {song_id})")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
import jieba
from musicdata import db
import math
from heapq import nsmallest
cur = db.cursor()

# 获取详细的歌曲信息
def get_song_details(song_ids):
    if not song_ids:
        return []

    format_strings = ','.join(['%s'] * len(song_ids))

    # 获取歌曲的基本信息
    sql = f"""
    SELECT s.SongID, s.SongName, s.Version, s.AlbumID, a.AlbumName ,s.Duration
    FROM songs s
    JOIN albums a ON s.AlbumID = a.AlbumID
    WHERE s.SongID IN ({format_strings})
    """
    cur.execute(sql, tuple(song_ids))
    songs = cur.fetchall()

    # 获取歌曲的艺术家信息
    sql = f"""
    SELECT p.SongID, ar.ArtistName
    FROM performances p
    JOIN artists ar ON p.ArtistID = ar.ArtistID
    WHERE p.SongID IN ({format_strings})
    """
    cur.execute(sql, tuple(song_ids))
    artists = cur.fetchall()

    # 构建一个字典以便快速查找每首歌的艺术家
    artist_dict = {}
    for song_id, artist_name in artists:
        if song_id in artist_dict:
            artist_dict[song_id].append(artist_name)
        else:
            artist_dict[song_id] = [artist_name]

    # 将艺术家信息添加到歌曲信息中
    detailed_results = []
    for song in songs:
        song_id, song_name, version, album_id, album_name,duration = song
        artist_names = artist_dict.get(song_id, [])
        detailed_results.append({
            'SongID': song_id,
            'SongName': song_name,
            'Version': version,
            'AlbumName': album_name,
            'Artists': artist_names,
            'Duration':duration
        })

    return detailed_results

#歌名
def songsearch_results(keysong):
    search_result = set()  # 使用 set 来自动去重
    keywords = keysong.split()  # 将输入字符串按空格分隔成单词列表

    for keyword in keywords:
        results = sql_query(keyword)
        # if results:
        #     print(f"Results for '{keyword}': {results}")
        search_result.update(results)  # 对每个关键字进行查询，并更新结果集

    # print(f"Final combined results: {search_result}")
    return list(search_result)  # 将 set 转换为 list 以便返回
def sql_query(keysong):
    sql = "select SongID from songs where SongName like '%%%%%s%%%%'" % keysong

    cur.execute(sql)
    result = cur.fetchall()
    # print(f"Raw query results: {result}")
    return result  # 返回原始结果列表


# 歌手
def artistsearch_results(keyartist):
    search_result = set()  # 使用 set 来自动去重
    keywords = keyartist.split()  # 将输入字符串按空格分隔成单词列表

    for keyword in keywords:
        results = sql_artistquery(keyword)
        if results:
            print(f"Results for '{keyword}': {results}")
        search_result.update(results)  # 对每个关键字进行查询，并更新结果集

    # print(f"Final combined results: {search_result}")
    return list(search_result)  # 将 set 转换为 list 以便返回
def sql_artistquery(key_artist):
    # 参数化的 SQL 查询，使用 JOIN 来从 performances 和 songs 表中获取相关的歌曲信息
    sql = """
    SELECT s.SongID
    FROM artists a
    JOIN performances p ON a.ArtistID = p.ArtistID
    JOIN songs s ON p.SongID = s.SongID
    WHERE a.ArtistName LIKE %s
    """
    # 使用 %s 作为占位符，之后传递一个包含 '%' + key_artist + '%' 的元组来安全地填充占位符
    cur.execute(sql, ('%' + key_artist + '%',))
    result = cur.fetchall()
    # print(f"Raw query results for artist '{key_artist}': {result}")
    return result  # 返回原始结果列表


# 专辑
def albumsearch_results(keyalbum):
    search_result = set()  # 使用 set 来自动去重
    keywords = keyalbum.split()  # 将输入字符串按空格分隔成单词列表

    for keyword in keywords:
        results = sql_albumquery(keyword)
        # if results:
        #     print(f"Results for '{keyword}': {results}")
        search_result.update(results)  # 对每个关键字进行查询，并更新结果集

    # print(f"Final combined results: {search_result}")
    return list(search_result)  # 将 set 转换为 list 以便返回
def sql_albumquery(key_album):
    # 参数化的 SQL 查询，使用 JOIN 来从 albums 和 songs 表中获取相关的歌曲信息
    sql = """
    SELECT s.SongID
    FROM albums a
    JOIN songs s ON a.AlbumID = s.AlbumID
    WHERE a.AlbumName LIKE %s
    """
    # 使用 %s 作为占位符，之后传递一个包含 '%' + key_album + '%' 的元组来安全地填充占位符
    cur.execute(sql, ('%' + key_album + '%',))
    result = cur.fetchall()
    # print(f"Raw query results for album '{key_album}': {result}")
    return result  # 返回原始结果列表


#版本

def versionsearch_results(key_version):
    search_result = []
    search_result.extend(sql_versionquery(key_version))
    return search_result

def sql_versionquery(key_version):
    # 参数化的 SQL 查询，从 songs 表中获取特定版本的歌曲信息
    sql = """
    SELECT SongID
    FROM songs
    WHERE Version LIKE %s
    """
    # 使用 %s 作为占位符，之后传递一个包含 '%' + key_version + '%' 的元组来安全地填充占位符
    cur.execute(sql, ('%' + key_version + '%',))
    result = cur.fetchall()
    return result

#获取单个歌曲详情
def get_song_detail_by_id(song_id):
    sql = """
    SELECT s.SongID, s.SongName, s.Version, a.AlbumName, s.Lyrics
    FROM songs s
    JOIN albums a ON s.AlbumID = a.AlbumID
    WHERE s.SongID = %s
    """
    cur.execute(sql, (song_id,))
    song = cur.fetchone()

    if not song:
        return None

    # 移除歌词前面的空行
    lyrics = song[4]
    if lyrics:
        lyrics = '\n'.join([line for line in lyrics.splitlines() if line.strip() != ''])

    song_detail = {
        'SongID': song[0],
        'SongName': song[1],
        'Version': song[2] if song[2] else "暂无",
        'AlbumName': song[3],
        'Lyrics': lyrics,
        'Artists': []
    }

    # 获取艺术家信息
    sql = """
    SELECT ar.ArtistName
    FROM performances p
    JOIN artists ar ON p.ArtistID = ar.ArtistID
    WHERE p.SongID = %s
    """
    cur.execute(sql, (song_id,))
    artists = cur.fetchall()

    for artist in artists:
        song_detail['Artists'].append(artist[0])

    return song_detail

#主要歌手简介
def get_artist_biography(artist_name):
    sql = """
    SELECT Biography
    FROM artists
    WHERE ArtistName = %s
    """
    cur.execute(sql, (artist_name,))
    artist = cur.fetchone()
    return artist[0] if artist else "暂无简介"


#情感
def sql_emotionquery(target_arousal, target_valence, song_ids=None):
    if song_ids:
        # 如果有传入的 song_ids 列表，则只对这些歌曲进行情感排序
        sql = """
        SELECT SongID, Arousal, Valence
        FROM songs
        WHERE SongID IN %s
        """
        cur.execute(sql, (tuple(song_ids),))
    else:
        # 否则对所有歌曲进行情感排序
        sql = """
        SELECT SongID, Arousal, Valence
        FROM songs
        """
        cur.execute(sql)

    results = cur.fetchall()

    # 计算每首歌的距离
    distance_results = []
    for result in results:
        song_id, arousal, valence = result
        distance = math.sqrt((target_arousal - arousal) ** 2 + (target_valence - valence) ** 2)
        distance_results.append((distance, song_id))

    # 找到距离最小的前 N 首歌
    closest_songs = nsmallest(10, distance_results)

    closest_song_ids = [song[1] for song in closest_songs]
    # print(f"Closest songs for Arousal={target_arousal}, Valence={target_valence}: {closest_song_ids}")
    return closest_song_ids


def emotionsearch_results(arousal, valence, song_ids=None):
    # 确保 arousal 和 valence 是有效的浮点数
    try:
        arousal = float(arousal)
        valence = float(valence)
    except ValueError:
        return []

    return sql_emotionquery(arousal, valence, song_ids)


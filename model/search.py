import jieba
from musicdata import db
cur = db.cursor()

#歌名
def songsearch_results(keysong):
    search_result = []
    # # 取出待搜索keyword
    # keyword = request.form['keyword']
    # 对keyword分词
    #cut_keywords = jieba.cut_for_search(keyword)
    # 遍历所有切分出来的词，搜索数据库
    #for cut_keyword in cut_keywords:
    #  search_result.extend(sql_query(cut_keyword))
    # 记录搜到了多少数据
    #search_result = set(search_result)
    search_result.extend(sql_query(keysong))
    return search_result
def sql_query(keysong):
    sql= "select SongID,SongName,Duration,Version,AlbumID from songs where SongName like '%%%%%s%%%%'" % keysong
    cur.execute(sql)
    result=cur.fetchall()
    return result

#歌手
def artistsearch_results(keyartist):
    search_result = []
    search_result.extend(sql_artistquery(keyartist))
    return search_result
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
    return result

#专辑
def albumsearch_results(keyalbum):
    search_result = []
    search_result.extend(sql_albumquery(keyalbum))
    return search_result

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
    return result

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




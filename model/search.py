import jieba
from musicdata import db
cur = db.cursor()
def search_results(keyword):
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
    search_result.extend(sql_query(keyword))
    return search_result

def sql_query(keyword):

    sql= "select SongID,SongName,Duration,Version,AlbumID from songs where SongName like '%%%%%s%%%%'" % keyword
    cur.execute(sql)
    result=cur.fetchall()
    return result


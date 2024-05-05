def sql_query(keyword):
    sql= "select SongName from songs where song_name like '%{keyword}%'".format(keyword=keyword)
    cursor.execute(sql)
    result=cursor.fetchall()
    return result


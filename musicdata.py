import pymysql

# 连接数据库，此前在数据库中创建数据库yuketang
db = pymysql.connect(host="localhost", user="root", password="123456", db="music",charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()


# 歌曲类
class Songs:
    def __init__(self, SongID, SongName, Duration, Version, AlbumID, Lyrics):
        self.SongID=SongID
        self.SongName = SongName
        self.Duration = Duration
        self.Version = Version
        self.AlbumID = AlbumID
        self.Lyrics = Lyrics

    # # 按歌曲编号查询歌曲的全部信息
    # def search_datas(self):
    #     # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
    #     db.ping(reconnect=True)
    #     # 插入sql语句
    #     sql = "SELECT * FROM Songs WHERE SongID='" + self.SongID+ "'"
    #     # 执行sql语句
    #     cursor.execute(sql)
    #     results1 = cursor.fetchone()
    #     results = []
    #     for item in results1:
    #         results.append(item)
    #     # 关闭数据库
    #     db.close()
    #     # 返回结果
    #     return results

    # 修改歌曲信息
    def update_datas(self):
        # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
        db.ping(reconnect=True)
        # 插入sql语句
        sql = "UPDATE songs SET SongName='" + self.SongName + "',Duration='" + self.Duration + "',Version='" + self.Version + "', \
                                                                                                            AlbumID='" + self.AlbumID + "',lyrics='" + self.Lyrics + "' WHERE SongID='" + self.SongID + "'"
        # 执行sql语句
        cursor.execute(sql)
        db.commit()
        db.close()

    # 添加歌曲的信息
    def add_datas(self):
        # ping()使用该方法 ping(reconnect=True)
        db.ping(reconnect=True)
        # 编写sql语句
        sql_0 = "INSERT INTO Songs(SongID, SongName, Duration, Version, AlbumID, lyrics) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        sql = sql_0 % (repr(self.SongID), repr(self.SongName), repr(self.Duration), repr(self.Version), repr(self.AlbumID),
                       repr(self.Lyrics))
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 关闭数据库
        db.close()

    # 删除歌曲的信息
    def delete_data(self):
        # ping()使用该方法 ping(reconnect=True)
        db.ping(reconnect=True)
        sql = "DELETE FROM students WHERE SongID='" + self.SongID + "' "
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 关闭数据库
        db.close()

#歌手类
class artists:
    def __init__(self,ArtistID,ArtistName):
        self.ArtistID = ArtistID
        self.ArtistName = ArtistName

#专辑类
class albums:
    def __init__(self,AlbumID,AlbumName,ArtistID):
        self.AlbumID= AlbumID
        self.AlbumName = AlbumName
        self.ArtistID= ArtistID



"""
    def search_course(self):
        # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
        db.ping(reconnect=True)
        # 插入sql语句
        sql = "SELECT *  FROM course WHERE snum='" + self.snum + "'"
        # 执行sql语句
        cursor.execute(sql)
        results1 = cursor.fetchone()
        results = []
        for item in results1:
            results.append(item)
        # 关闭数据库
        db.close()
        # 返回结果
        return results

    # 修改学生选课
    def update_course(self):
        # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
        db.ping(reconnect=True)
        # 插入sql语句
        sql = "UPDATE course  SET course1='" + self.course1 + "',course2='" + self.course2 + "',course3='" + self.course3 + "',course4='" + self.course4 + "'WHERE snum='" + self.snum + "'"
        # 执行sql语句
        cursor.execute(sql)
        db.commit()
"""
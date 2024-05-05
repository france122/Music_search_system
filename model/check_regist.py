from musicdata import db

cur = db.cursor()

def add_user(username, password):
    # sql commands
    sql = "INSERT INTO user(username, password) VALUES ('%s','%s')" %(username, password)
    # execute(sql)
    cur.execute(sql)
    # commit
    db.commit()  # 对数据库内容有改变，需要commit()
    db.close()

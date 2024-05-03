import musicdata as mud
from flask import request, session
# 登录功能
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username != 'admin':
        return '账号错误，请重新输入！'
    else:
        if password == '123456':
            session['username'] = username
            return 1
        else:
            return "密码错误，请重新登录"


# 按SongID查找歌曲的全部信息
# def search_songid_data(SongID):
#     return mud.Songs(SongID,'','','', '','').search_datas()


# 修改歌曲信息
def update_data():
    st = []
    lst = ['SongName','Duration','Version','AlbumID','lyrics']
    for item in lst:
        st.append(request.form.get(f'{item}'))
    mud.Songs(SongID, st[0], st[1], st[2], st[3], st[4],st[5]).update_datas()


# 添加歌曲信息
def add_data():
    lst = ['SongID', 'SongName','Duration','Version','AlbumID','lyrics']
    data_lst = []
    for item in lst:
        data_lst.append(request.form.get(f'{item}'))
    mud.Songs(data_lst[0], data_lst[1], data_lst[2], data_lst[3],
                data_lst[4], data_lst[5],).add_datas()



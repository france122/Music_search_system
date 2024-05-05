import musicdata as mud
from flask import request, session


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



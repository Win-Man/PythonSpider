from bs4 import BeautifulSoup
import requests
import re
from modules import CloudMusic_playlist
import time

s = requests.session()
playlist_base_url = 'http://music.163.com/discover/playlist/'
cloud_music_base_url = 'http://music.163.com'
playlist_url = 'http://music.163.com/#/playlist'

cloud_music_headers = {
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Connection': 'keep-alive'
}

# 获取所有歌单标签
def getAllPlayListTags():
    tag_response = s.get(playlist_base_url,headers=cloud_music_headers)
    tag_html = tag_response.text
    print(tag_html)
    tag_soup = BeautifulSoup(tag_html, 'html.parser')
    tag_a_list = tag_soup.find_all('a', class_='s-fc1 ')
    tag_list = []
    for a in tag_a_list:
        tag_list.append(a.text)
    for i in range(len(tag_list)):
        if tag_list[i] == '游戏':
            tag_list = tag_list[i:]
            break
    return tag_list

# 获取所有的歌单
def getAllPlaylist():
    play_list_params = {
        'order': 'hot',
        'cat': '全部',
        'limit': 35,
        'offset': 0
    }
    tag_list = getAllPlayListTags()
    for tag in tag_list:
        play_list_params['cat'] = tag
        play_list_params['offset'] = 0
        while True:
            print('正在下载页面:')
            print(play_list_params)
            playlist_response = s.get(playlist_base_url,params=play_list_params,headers=cloud_music_headers)
            playlist_html = playlist_response.text
            playlist_list = parserAllPlayList(playlist_html)
            if len(playlist_list) == 0:
                break
            play_list_params['offset'] += play_list_params['limit']
            print('页面下载完成')
            time.sleep(3)


# 对歌单页面进行解析
def parserAllPlayList(playlist_html):
    playlist_soup = BeautifulSoup(playlist_html,'html.parser')
    playlist_container = playlist_soup.find(attrs={'id': 'm-pl-container'})
    playlist_list = []
    if playlist_container:
        playlist_list = playlist_container.find_all('li')
        for playlist in playlist_list:
           parserPlaylistInfo(playlist)
    return playlist_list


def parserPlaylistInfo(playlist):
    print('正在解析歌单信息:')
    playlist_data={
        'cover_url': '',
        'play_num': '',
        'name': '',
        'playlist_id': '',
        'create_user_id': ''
    }
    playlist_data['cover_url'] = playlist.find('img')['src']
    playlist_data['name'] = playlist.find('p').find('a')['title']
    num_pattern = re.compile(r'(\d*)')
    playlist_id_pattern = re.compile(r'/playlist\?id=(\d*)')
    playlist_id_search = playlist_id_pattern.search(str(playlist))
    if playlist_id_search:
        # print('playlist_id_search:')
        # print(playlist_id_search.group(1))
        playlist_data['playlist_id'] = str(playlist_id_search.group(1)) if playlist_id_search else ''
    user_id_pattern = re.compile(r'/user/home\?id=(\d*)')
    user_id_search = user_id_pattern.search(str(playlist))
    if user_id_search:
        # print('user_id_search:')
        # print(user_id_search.group(1))
        playlist_data['create_user_id'] = str(user_id_search.group(1)) if user_id_search else ''
    playlist_data['play_num'] = str(playlist.find('span', class_='nb').text)
    print('歌单信息解析完成,歌单信息为:')
    print(playlist_data)
    print('正在保存歌单信息')
    savePlaylistData(playlist_data)
    print('保存歌单信息完成')

# 保存歌单信息
def savePlaylistData(data):
    if data:
        try:
            playlist = CloudMusic_playlist.get(CloudMusic_playlist.playlist_id == data.get('playlist_id'))
            print('正在更新歌单信息......')
            playlist.cover_url = data.get('cover_url')
            playlist.play_num = data.get('play_num')
            playlist.name = data.get('name')
            playlist.playlist_id = data.get('playlist_id')
            playlist.create_user_id = data.get('create_user_id')
            playlist.save()
        except Exception as e:
            print('正在保存新歌单......')
            playlist = CloudMusic_playlist(cover_url=data.get('cover_url'), play_num=data.get('play_num'), name=data.get('name'), playlist_id=data.get('playlist_id'), create_user_id=data.get('create_user_id'))
            playlist.save()



if __name__ == '__main__':
    getAllPlaylist()
    #music_response = s.get('http://113.215.16.36/m10.music.126.net/20160823175519/896be39e14daf633aee75f365efabef4/ymusic/0302/759e/fe20/28c89f0f93aa674ef6997be6971d4893.mp3?wshc_tag=0&wsts_tag=57bc17c0&wsid_tag=71d7153b&wsiphost=ipdbm')
    #with open('123.mp3','wb') as f:
     #   f.write(music_response.content)
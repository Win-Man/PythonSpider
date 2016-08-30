import time
import requests
from bs4 import BeautifulSoup
from modules import Jianshu_people
s = requests.session()
seed_url='/users/dd76eadb5359'
base_url = 'http://www.jianshu.com'
urls=[]

jianshu_headers={
    'Host': 'www.jianshu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}
def getFollowers(people_url):
    follower_url = base_url+people_url+'/followers'
    page = 1
    while True:
        t = int(time.time()*1000)
        follower_data = {
            'page':page,
            '_':t
        }
        follower_response = s.get(follower_url, data=follower_data, headers=jianshu_headers, timeout=9)
        #print(follower_response.text)
        return_url = followResponseParser(follower_response.text)
        if len(return_url) == 0:
            break
        page += 1
def getFollowings(people_url):
    following_url = base_url+people_url+'/following'
    page = 1
    while True:
        t = int(time.time()*1000)
        following_data = {
            'page': page,
            '_': t
        }
        following_response = s.get(following_url, data=following_data, headers=jianshu_headers, timeout=9)
        #print(follower_response.text)
        return_url = followResponseParser(following_response.text)
        if len(return_url) == 0:
            break
        page += 1

#通过每次请求，获取被关注列表中用户的地址并返回
def followResponseParser(response_text):
    time.sleep(1)
    follower_soup = BeautifulSoup(response_text,'html.parser')
    user_ul = follower_soup.find('ul',class_='users')
    users = user_ul.find_all('li')
    user_url = []
    for user_li in users:
        avatar = user_li.find('a',class_='avatar')
        if avatar:
            user_url.append(avatar['href'])
    print(user_url)
    if len(user_url):
        with open('todo.txt','a') as f:
            for url in user_url:
                if len(url.strip()):
                    f.write(url.strip())
                    f.write('\n')
    return user_url

#分析用户主页面
def userHomeParser(user_url):
    home_url = base_url+user_url+'/latest_articles'
    home_response = s.get(home_url,headers=jianshu_headers,timeout=9)
    home_soup = BeautifulSoup(home_response.text, 'html.parser')
    base_info_div = home_soup.find('div', class_='basic-info')
    user_stats_div = home_soup.find('div', class_='user-stats')
    user_data={}
    if base_info_div:
        user_data['avatar_url'] = base_info_div.find('img')['src']
        user_data['name'] = base_info_div.find('h3').find('a').get_text()
        jianshu_id = base_info_div.find('h3').find('a')['href']
        jianshu_id = jianshu_id[7:]
        user_data['jianshu_id'] = jianshu_id
    if user_stats_div:
        lis = user_stats_div.find_all('li')
        user_data['subscriptions'] = lis[0].find('b').get_text()
        user_data['followers'] = lis[1].find('b').get_text()
        user_data['posts'] = lis[2].find('b').get_text()
        user_data['words'] = lis[3].find('b').get_text()
        user_data['gain_love'] = lis[4].find('b').get_text()
    print(user_data)
    if user_data:
        people = Jianshu_people(avatar_url=user_data.get('avatar_url'),name=user_data.get('name'),jianshu_id=user_data.get('jianshu_id'),subscriptions=user_data.get('subscriptions'),followers=user_data.get('followers'),posts=user_data.get('posts'),words=user_data.get('words'),gain_love=user_data.get('gain_love'))
        people.save()
        print('保存成功')
    else:
        return

if __name__ == '__main__':
    # getFollowings(seed_url)
    # print(len(urls))
    #userHomeParser(seed_url)
    todo_urls = []
    while True:
        with open('todo.txt','r') as f:
            todo_urls = f.readlines()
        # print('todo_urls_before:')
        # print(todo_urls)
        if len(todo_urls) == 0:
            print('结束')
            break
        todo_urls = list(set(todo_urls))
        current_url = todo_urls[0].strip()
        todo_urls=todo_urls[1:]
        # print('todo_urls:')
        # print(todo_urls)
        print('current_url'+current_url)
        with open('todo.txt','w') as f:
            for url in todo_urls:
                if len(url.strip()):
                    f.write(url.strip())
                    f.write('\n')
        if len(current_url) == 0:
            continue
        done_urls = []
        with open('done.txt','r') as f:
            done_urls = f.readlines()
        flag = False
        for done_url in done_urls:
            if done_url.strip() == current_url:
                flag = True
                break
        if flag:
            continue
        try:
            print('当前解析:'+current_url)
            userHomeParser(current_url)
            print('解析结束')
            with open('done.txt','a') as f:
                f.write(current_url)
                f.write('\n')
            print('正在获取被关注列表')
            getFollowers(current_url)
            print('获取被关注列表完成')
            print('正在获取关注列表')
            getFollowings(current_url)
            print('获取关注列表完成')
            time.sleep(3)
        except requests.exceptions.ReadTimeout as e:
            print('超时休息')
            time.sleep(120)
            print('休息结束')
        except ConnectionError as ce:
            print('max retries exceeded with url')
            time.sleep(120)
            print('end')



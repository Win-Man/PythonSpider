import requests
from modules import Douban_movie
# tag = CharField()
#     douban_id = IntegerField()
#     url = CharField()
#     rate = DecimalField()
#     title = CharField()
#     is_new = BooleanField()
#     playable = BooleanField()
#     cover_img_url = CharField()
#     is_beetle_subject = BooleanField()
#     cover_x = IntegerField()
#     cover_y = IntegerField()
def saveDoubanMovies(tag,jsonMoviesList):
    for movie in jsonMoviesList:
        douban_id = int(movie['id'])
        url = movie['url']
        rate = float(movie['rate'])
        title = movie['title']
        is_new = movie['is_new']
        playable = movie['playable']
        cover_img_url = movie['cover']
        is_beetle_subject = movie['is_beetle_subject']
        cover_x = int(movie['cover_x'])
        cover_y = int(movie['cover_y'])
        save_movie = Douban_movie(tag=tag,douban_id=douban_id,url=url,rate=rate,title=title,is_new=is_new,playable=playable,cover_img_url=cover_img_url,is_beetle_subject=is_beetle_subject,cover_x=cover_x,cover_y=cover_y)
        save_movie.save()

if __name__ == '__main__':
    s = requests.Session()
    tag_url = 'https://movie.douban.com/j/search_tags'
    movies_url = 'https://movie.douban.com/j/search_subjects'
    movies_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'll="118172"; bid=5oPO_hDqjhg; ap=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1469938729%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __utma=30149280.1445189242.1469928825.1469928825.1469938730.3; __utmb=30149280.0.10.1469938730; __utmc=30149280; __utmz=30149280.1469938730.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1333366301.1469928825.1469928825.1469938730.2; __utmb=223695111.0.10.1469938730; __utmc=223695111; __utmz=223695111.1469938730.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=9a4366643a7fb795.1469928741.2.1469938742.1469933062.; _pk_ses.100001.4cf6=*',
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
    movies_params = {
        'type': 'movie',
        'tag': '华语',
        'sort': 'recommend',
        'page_limit': '20',
        'page_start': '0'
    }
    tag_params={
        'type':'movie',
    }
    tag_response = s.get(tag_url,headers = movies_headers,params = tag_params)
    print(tag_response.text)
    tags = tag_response.json()['tags']

    for tag in tags:
        count = 20
        movies_params['tag'] = tag
        movies_params['page_start'] = '0'
        while count > 0:
            movies_response = s.get(movies_url,headers = movies_headers,params = movies_params)
            movies_json = movies_response.json()
            count = len(movies_json['subjects'])
            if count < 20:
                break
            movies_params['page_start'] = int(movies_params['page_start']) + count
            print(tag +':' + movies_response.text )
            print(movies_json)
            saveDoubanMovies(tag,movies_json['subjects'])


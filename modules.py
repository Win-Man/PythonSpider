from peewee import *

db = MySQLDatabase(host='localhost', user='root', passwd='admin', database='test', charset='utf8', port=3306)



class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = db

# 'playable': False,
# 'is_beetle_subject': False,
# 'cover_y': 800,
# 'title': '上帝之城',
# 'id': '1292208',
# 'rate': '8.9',
# 'url': 'https: //movie.douban.com/subject/1292208/',
# 'cover_x': 600,
# 'cover': 'https: //img3.doubanio.com/view/movie_poster_cover/lpst/public/p455677490.jpg',
# 'is_new': False
class Douban_movie(Model):
    tag = CharField()
    douban_id = IntegerField()
    url = CharField()
    rate = DecimalField()
    title = CharField()
    is_new = BooleanField()
    playable = BooleanField()
    cover_img_url = CharField()
    is_beetle_subject = BooleanField()
    cover_x = IntegerField()
    cover_y = IntegerField()

    class Meta:
        database = db


class Douban_book(Model):
    book_url = CharField()
    book_name = CharField()
    book_cover_img_url = CharField()
    book_author = CharField()
    book_publish = CharField()
    book_publish_date = CharField()
    book_page_number = IntegerField()
    book_price = DecimalField()
    book_isbn = CharField()
    book_intro = TextField()
    book_translator = CharField()
    book_original_name = CharField()

    class Meta:
        database = db


class Zhihu_people(Model):
    index_url = CharField()
    name = CharField()
    avatar_url = CharField()
    agree = IntegerField()
    thanks = IntegerField()
    asks = IntegerField()
    answers = IntegerField()
    posts = IntegerField()
    collections = IntegerField()
    logs = IntegerField()
    followees = IntegerField()
    followers = IntegerField()
    sex = CharField()
    location = CharField()

    class Meta:
        database = db

class Jianshu_people(Model):
    jianshu_id = CharField()
    avatar_url = CharField()
    name = CharField()
    subscriptions = IntegerField()
    followers = IntegerField()
    posts = IntegerField()
    words = IntegerField()
    gain_love = IntegerField()

    class Meta:
        database = db





if __name__ == '__main__':
    db.connect()
    db.create_tables([CloudMusic_playlist])
import requests
import re
import time
import datetime
from bs4 import BeautifulSoup
from modules import Douban_book
s = requests.session()
book_info_headers = {
    'Connection': 'keep-alive',
    'Host': 'book.douban.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'
}
base_url = 'https://book.douban.com'


#获取所有图书的标签类别
def getBooktags():
    tag_url = 'https://book.douban.com/tag'
    tag_param = {'icn': 'index-nav'}
    tag_response = s.get(tag_url, params=tag_param,headers=book_info_headers)
    tag_soup = BeautifulSoup(tag_response.text, 'html.parser')
    tag_tables = tag_soup.find_all('table', class_='tagCol')
    for table in tag_tables:
        tag_a_urls = table.find_all('a')
        for url in tag_a_urls:
            with open('tag_todo.txt','a') as f:
                f.write(url['href'])
                f.write('\n')
    print(tag_response.text)

#获取所有图书的url地址
def getBookUrls():
    while True:
        with open('tag_todo.txt','r') as tf:
            if len(tf.readlines()) == 0:
                break
        current_tag_url = ''
        with open('tag_doing.txt', 'r') as f:
            if len(f.readlines()):
                current_tag_url = base_url+f.readlines()[0].strip()
            else:
                urls = []
                with open('tag_todo.txt','r') as tf:
                    urls = tf.readlines()
                    current_tag_url = base_url + urls[0].strip()
                urls = urls[1:]
                with open('tag_todo.txt','w') as tf:
                    for url in urls:
                        tf.write(url.strip())
                        tf.write('\n')
        with open('tag_doing.txt','wb') as f:
            f.write(str.encode(current_tag_url))
        tag_book_params={
            'start': 0,
            'type': 'T'
        }
        print('正在下载标签:'+current_tag_url)
        while True:
            books_response = s.get(current_tag_url,headers=book_info_headers,params=tag_book_params)
            books_soup = BeautifulSoup(books_response.text, 'html.parser')
            book_items = books_soup.find('ul', class_='subject-list').find_all('li')
            if len(book_items) == 0:
                break
            print(tag_book_params)
            for item in book_items:
                book_item_url = item.find('div', class_='pic').find('a')['href']
                if book_item_url != None:
                    with open('book_url_todo.txt', 'a') as butf:
                        butf.write(book_item_url)
                        butf.write('\n')
            tag_book_params['start'] += 20
            time.sleep(3)
        with open('tag_doing.txt', 'w') as f:
            f.truncate()
        with open('tag_done.txt', 'a') as tdf:
            tdf.write(current_tag_url)
            tdf.write('\n')
        print('下载完成:'+current_tag_url)


#解析图书信息
def bookInfoParder(book_url):
    book_response = s.get(book_url,headers=book_info_headers)
    print(book_response)
    book_soup = BeautifulSoup(book_response.text,'html.parser')
    book_info_html = book_soup.find('div', id='info').get_text()
    book_name = book_soup.find('h1').find('span').get_text()
    book_cover_img_url = book_soup.find('div', id='mainpic').find('img')['src']
    book_intro = book_soup.find('div', class_='intro').get_text()
    book_data= {
        'book_url': '',
        'book_name': '',
        'book_cover_img_url': book_cover_img_url,
        'book_author': '',
        'book_publish': '',
        'book_publish_date': None,
        'book_page_number': 0,
        'book_price': 0.0,
        'book_isbn': '',
        'book_intro': '',
        'book_translator': '',
        'book_original_name': ''
    }
    book_data['book_url'] = book_url
    book_data['book_name'] = book_name
    book_data['book_cover_img_url'] = book_cover_img_url
    book_data['book_intro'] = book_intro
    print(book_info_html)
    #作者
    author_pattern = re.compile(r'作者:((\s*)(.*)(\s*)/)*(\s*)(.*)(\s*)')
    author_search = author_pattern.search(book_info_html)
    if author_search:
        index = author_search.group(0).find(':')
        book_author = author_search.group(0)[index+1:]
        book_author = book_author.split('/')
        for i in range(len(book_author)):
            book_author[i] = book_author[i].strip()
        book_author = '|'.join(book_author)
        book_data['book_author'] = book_author.strip()
    #出版社
    publish_pattern = re.compile(r'出版社:(\s*)(.*)(\s*)')
    publish_search = publish_pattern.search(book_info_html)
    if publish_search:
        index = publish_search.group(0).find(':')
        book_publish = publish_search.group(0)[index+1:]
        book_data['book_publish'] = book_publish.strip()
    #出版时间
    publish_date_pattern = re.compile(r'出版年:(\s*)(.*)(\s*)')
    publish_date_search = publish_date_pattern.search(book_info_html)
    if publish_date_search:
        index = publish_date_search.group(0).find(':')
        book_publish_date = publish_date_search.group(0)[index+1:]
        book_data['book_publish_date'] = book_publish_date.strip()
    #页数
    page_number_pattern = re.compile(r'页数:(\s*)(\d*)(\s*)')
    page_number_search = page_number_pattern.search(book_info_html)
    if page_number_search:
        index = page_number_search.group(0).find(':')
        book_page_number = page_number_search.group(0)[index+1:]
        book_data['book_page_number'] = int(book_page_number.strip())
    #价格
    price_pattern = re.compile(r'定价:(\s*)([0-9.]*)(\s*)')
    price_search = price_pattern.search(book_info_html)
    if price_search:
        index = price_search.group(0).find(':')
        book_price = price_search.group(0)[index+1:]
        book_data['book_price'] = float(book_price.strip())
    #isbn
    isbn_pattern = re.compile(r'ISBN:(\s*)(\d*)(\s*)')
    isbn_search = isbn_pattern.search(book_info_html)
    if isbn_search:
        index = isbn_search.group(0).find(':')
        book_isbn = isbn_search.group(0)[index+1:]
        book_data['book_isbn'] = book_isbn.strip()
    #译者
    translator_pattern = re.compile(r'译者:((\s*)(.*)(\s*)/)*(\s*)(.*)(\s*)')
    translator_search = translator_pattern.search(book_info_html)
    if translator_search:
        index = translator_search.group(0).find(':')
        book_translator = translator_search.group(0)[index+1:]
        book_translator = book_translator.split('/')
        for i in range(len(book_translator)):
            book_translator[i] = book_translator[i].strip()
        book_translator = '|'.join(book_translator)
        book_data['book_translator'] = book_translator.strip()
    #原作名
    original_name_pattern = re.compile(r'原作名:(\s*)(.*)(\s*)')
    original_name_search = original_name_pattern.search(book_info_html)
    if original_name_search:
        index = original_name_search.group(0).find(':')
        book_original_name = original_name_search.group(0)[index+1:]
        book_data['book_original_name'] = book_original_name.strip()
    print(book_data)
    saveBookInfo(book_data)

def saveBookInfo(book_data):
    save_book = Douban_book(book_url=book_data.get('book_url'), book_name=book_data.get('book_name'), book_cover_img_url=book_data.get('book_cover_img_url'), book_author=book_data.get('book_author'), book_publish=book_data.get('book_publish'), book_publish_date=book_data.get('book_publish_date'), book_page_number=book_data.get('book_page_number'), book_price=book_data.get('book_price'), book_isbn=book_data.get('book_isbn'), book_intro=book_data.get('book_intro'), book_translator=book_data.get('book_translator'), book_original_name=book_data.get('book_original_name'))
    save_book.save()

if __name__ == '__main__':
    # with open('tag_doing.txt', 'w') as f:
    #     f.write('')
    # getBooktags()
    getBookUrls()

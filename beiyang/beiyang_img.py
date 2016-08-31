from bs4 import BeautifulSoup
import requests
import re

s = requests.session()
index_url = 'http://www.ssyer.com/'
beiyang_headers={
    'Host': 'www.ssyer.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Connection': 'keep-alive'
}

def loopPage(pageCount):
    for i in range(pageCount):
        page_url = index_url+'/index_page_'
        page_url += str(i+1)
        page_url += '.html'
        print('正在下载页面'+str(i+1)+'的图片')
        parserPage(page_url)
        print('页面'+str(i+1)+'下载完成')

def parserPage(url):
    page_response = s.get(url,headers=beiyang_headers)
    page_html = page_response.text
    page_soup = BeautifulSoup(page_html,'html.parser')
    box_list = page_soup.find_all('div',class_='box_download')
    for box in box_list:
        img_url = index_url
        img_url += box.find('a')['href']
        print('正在下载图片：'+img_url)
        downloadImg(img_url)
        print('下载完成')

def downloadImg(url):
    img_response = s.get(url)
    img_name = url.split('/')[-1]
    if len(img_name) > 0:
        with open(img_name,'wb') as f:
            f.write(img_response.content)


def getPageNum():
    result = 0
    index_response = s.get(index_url,headers=beiyang_headers)
    index_response.encoding='utf-8'
    index_html = index_response.text
    num_content_pattern = re.compile(r'页，共(\d*)页')
    num_content_search = num_content_pattern.search(index_html)
    if num_content_search:
        print(num_content_search.group(0))
        num_pattern = re.compile(r'(\d*)')
        num_search = num_pattern.search(str(num_content_search.group(1)))
        if num_search:
            print(num_search.group(0))
            result = num_search.group(0)
    else:
        print('未找到')
    return int(result)

if __name__ == '__main__':
    page_num = getPageNum()
    loopPage(page_num)
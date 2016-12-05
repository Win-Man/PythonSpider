# coding=utf-8
from bs4 import BeautifulSoup
import requests
import os
import time

s = requests.session()
meizitu_headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36'
}

def getHtml(url):
    response = s.get(url,headers = meizitu_headers)
    if response.status_code == 200:
        return response.text
    return None

def getSoup(text):
    soup = BeautifulSoup(text,'html.parser')
    return soup

def downloadPic(page):

    try:
        url = 'http://jandan.net/ooxx/page-%s' %(page)
        text = getHtml(url)
        if text == None:
            return
        #print text
        soup = getSoup(text)
        lis = soup.find_all('div',class_='text')
        for li in lis:
            #print li
            if li.find('p') != None :
                if li.find('p').find('a') != None:
                    pic_url = li.find('p').find('a')['href']
                    saveImg(pic_url)
            else:
                print 'find img is None'
    except Exception as e:
        print e



def saveImg(img_url):
    print 'downloading pic:%s' %(img_url)
    response = s.get(img_url)
    if response.status_code == 200:
        pic_name = img_url.split('/')[-1]
        with open(os.path.join("E:\\pics",pic_name),'wb') as f:
            f.write(response.content)

if __name__ == '__main__':
    while True:
        page = 1
        with open('doing.txt','r') as f:
            page = f.readlines()[0]

        if int(page) == 0:
            break
        print 'dealing with page %s' %(page)
        downloadPic(page)

        with open('doing.txt','w') as f:
            f.write(str(int(page)-1))

        print 'rest 20s'
        time.sleep(20)
        print 'rest done'
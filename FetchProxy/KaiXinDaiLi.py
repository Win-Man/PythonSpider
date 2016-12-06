# coding=utf-8
import requests
from bs4 import BeautifulSoup

s = requests.session()

def getHtml(url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 54.0.2840.59 Safari / 537.36'
    }
    response = s.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def getSoup(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup

def getContinentsHign():
    count = 0
    for i in range(1, 11):
        url = 'http://www.kxdaili.com/dailiip/1/%d.html' %(i)
        text = getHtml(url)
        if text != None:
            soup = getSoup(text)
            trs = soup.find('table', class_='table').find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                print '%s %s %s' %(tds[0].text, tds[1].text, tds[3].text)
                count = count + 1

    print 'find %d proxies' %(count)

def getContinentsCommon():
    count = 0
    for i in range(1, 11):
        url = 'http://www.kxdaili.com/dailiip/2/%d.html' %(i)
        text = getHtml(url)
        if text != None:
            soup = getSoup(text)
            trs = soup.find('table', class_='table').find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                print '%s %s %s' %(tds[0].text, tds[1].text, tds[3].text)
                count = count + 1

    print 'find %d proxies' %(count)

def getOverseaHigh():
    count = 0
    for i in range(1, 11):
        url = 'http://www.kxdaili.com/dailiip/3/%d.html' %(i)
        text = getHtml(url)
        if text != None:
            soup = getSoup(text)
            trs = soup.find('table', class_='table').find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                print '%s %s %s' %(tds[0].text, tds[1].text, tds[3].text)
                count = count + 1

    print 'find %d proxies' %(count)

def getOverseaCommon():
    count = 0
    for i in range(1, 11):
        url = 'http://www.kxdaili.com/dailiip/4/%d.html' %(i)
        text = getHtml(url)
        if text != None:
            soup = getSoup(text)
            trs = soup.find('table', class_='table').find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                print '%s %s %s' %(tds[0].text, tds[1].text, tds[3].text)
                count = count + 1

    print 'find %d proxies' %(count)

if __name__ == '__main__':
    getContinentsHign()
    getContinentsCommon()
    getOverseaHigh()
    getOverseaCommon()
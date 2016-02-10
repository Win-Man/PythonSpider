#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import cookielib,urllib,base64,rsa,binascii,re

head ={'Accept':'*/*',
           'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With':'XMLHttpRequest',
           'Referer':'http://www.zhihu.com',
           'Accept-Language':'zh-CN',
           'Accept-Encoding':'gzip, deflate',
           'User-Agent':'Mozilla/5.0(Windows NT 6.1;WOW64;Trident/7.0;rv:11.0)like Gecko',
           'Host':'www.zhihu.com'}
class Login(object):
    def login_zhihu(self,email,password):
        url = "http://www.zhihu.com"
        s = requests.session()

        #如果已经登录过，那就可以直接使用cookies登录
        if os.path.exists("cookies.txt"):
            #实例化一个LWPCookieJar对象
            load_cookiejar = cookielib.LWPCookieJar()
            #从文件中加载cookies(LWP格式)
            load_cookiejar.load('cookies.txt', ignore_discard=True, ignore_expires=True)
            #工具方法转换成字典
            load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
            #工具方法将字典转换成RequestsCookieJar，赋值给session的cookies.
            s.cookies = requests.utils.cookiejar_from_dict(load_cookies)
            if s.get(url).status_code == 200:
                return s


        html = s.get(url)

        soup = BeautifulSoup(html.text,'html.parser')
        xrsf = soup.find('input')

        ##验证码
        yanzhen_url = 'https://www.zhihu.com/captcha.gif?r='+str(int(time.time()*1000))
        haha = s.get(yanzhen_url,headers = head)

        with open('code.jpg','wb') as f:
            f.write(haha.content)
        print '请输入验证码'
        yanzhen = raw_input()

        print '验证码:'+yanzhen

        login_data = {'_xsrf':xrsf,
                      'password':password,
                      'captcha':yanzhen,
                      'email':email,
                      'remember_me':'true'}

        r = s.post('https://www.zhihu.com/login/email',data=login_data,headers = head)
        print r.text


        #实例化一个LWPcookiejar对象
        new_cookie_jar = cookielib.LWPCookieJar('cookies.txt')
        #将转换成字典格式的RequestsCookieJar保存到LWPcookiejar中
        requests.utils.cookiejar_from_dict({c.name: c.value for c in s.cookies}, new_cookie_jar)
        #保存到本地文件
        new_cookie_jar.save('cookies.txt', ignore_discard=True, ignore_expires=True)
        return s

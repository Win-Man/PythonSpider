#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import cookielib,urllib,base64,rsa,binascii,re

head_sina = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'Origin':'http://weibo.com',
        "Referer":"http://weibo.com/",
        'User-Agent':'Mozilla/5.0(Windows NT 6.1;WOW64;Trident/7.0;rv:11.0)like Gecko',
        'Host':'login.sina.com.cn'}

data_sina = {
    "entry":"weibo",
    "gateway":"1",
    "savestate":"7",
    "useticket":"1",
    "pagerefer":"https://www.baidu.com/link?url=3YSdEuAbjIWO9udn3LjIow1nWKq68fuNgSft3DzFvJu&wd=&eqid=91465358014ef6870000000356b9ac4e",
    "vsnf":"1",
    "su":"emhlZGFwYXQlNDAxNjMuY29t",
    "service":"miniblog",
    "servicetime":"1455008896",
    "nonce":"",
    "pwencode":"rsa2",
    "rsakv":"1330428213",
    "sp":"12111dccf90c3bcf75e7e8dbe4577a42af9f9890b3dab3ec43e224585922679f0d855caef9fa5040da784387e86e2914f978a75eb0e9e73393d6ae78953db72e9354b05641c86ef2c1c459e31e7fcb508362d5e72d32da421aefcc8397c49b3416039e9dbd38aa3710caca4be31822fc5fbe7146cb7b64f0d35dd0db70856b3b",
    "sr":"1366*768",
    "encoding":"UTF-8",
    "prelt":"76",
    "url":"http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
    "returntype":"META"
}




class Login(object):
    def login_sina(self,email,password):
        pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=emhlZGFwYXQlNDAxNjMuY29t&rsakt=mod&client=ssologi"
        s = requests.session()

        res=s.get(pre_url)
        res = res.text.encode('utf-8').split('(')[-1].split(')')[0]
        pre_json = json.loads(res)
        print pre_json
        servertime = pre_json['servertime']
        nonce = pre_json['nonce']
        rsakv = pre_json['rsakv']
        pubkey = pre_json['pubkey']
        #urllib.quote()是进行url编码
        #su是经过一次base64加密之后的账号
        su = base64.encodestring(urllib.quote(email))[:-1]
        print "su:%s" % su
        #rsa2计算sp
        rsaPubkey = int(pubkey,16)
        key = rsa.PublicKey(rsaPubkey,65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        sp = rsa.encrypt(message,key)
        sp = binascii.b2a_hex(sp)
        print "sp:%s" % sp
        data_sina['servertime'] = servertime
        data_sina['nonce'] = nonce
        data_sina['rsakv'] = rsakv
        data_sina['su'] = su
        data_sina['sp'] = sp

        #
        post_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&wsseretry=servertime_error"
        res = s.post(post_url,data = data_sina)
        #print res.text

        p = re.compile('location\.replace\(\'(.*?)\'\)')

        final_url = p.search(res.text.encode('utf-8')).group(1)
        res = s.get(final_url)
        #print res.text
        res = res.text.encode('utf-8').split('(')[-1].split(')')[0]
        user_json = json.loads(res)
        uniqueid = user_json['userinfo']['uniqueid'].encode('utf-8')
        #print user_json['userinfo']['uniqueid']


        return s

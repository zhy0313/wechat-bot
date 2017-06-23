#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/20 0020 23:59
# @Author  : Labulaka
# @Mail     :labulaka521@live.cn
# @FileName    : itchat_api_news.py
'''使用多线程'''
import urllib2,re,requests,json,time,threading
new_url = "http://www.chinanews.com/scroll-news/news1.html"
lock = threading.Lock()

def G_code(url):
    '''获取页面源码'''
    user_agent = {"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"}
    headers = {"User-Agent":user_agent}
    request = urllib2.Request(url,headers = headers)
    text = urllib2.urlopen(request).read()
    text = text.decode('gbk').encode('utf-8')
    return text
def Short_Url(code):
    '用''返回时间标题新浪url信息，使多线程同时执行'''
    url_api = "https://api.weibo.com/2/short_url/shorten.json"
    payload = {
        "source":5786724301,
        "url_long":"http://"+code[0]
    }
    r = requests.get(url_api,params=payload)
    text = json.loads(r.text)
    lock.acquire()
    for i in text:
        msg.append(code[2]+code[1]+str(text[i][0]['url_short'])+"\n")
    lock.release()
class News():
    '''获取最新新闻消息'''
    def __init__(self,num):
        '''num 是总共获取的新闻数量,默认为10'''
        if  num:
            self.num = num
        else:
            self.num = 10

    def Get_Link(self):
        '''得到标题和原始链接'''
        code = G_code(new_url)
        Link = []
        pattern = re.compile(r'<div class="dd_bt"><a href="//(.*?)">(.*?)</a></div>.*?<div class="dd_time">(.*?)</div>',re.S)
        for item in re.findall(pattern,code):
            if self.num > 0:
                Link.append(item)
            self.num = int(self.num) - 1
        return Link
    def run(self):
        '''获取新闻标题及相应的短连接'''
        code = News(self.num).Get_Link()
        global msg
        msg = []
        threads = []        #线程列表
        title = []          #标题
        for i in range(int(self.num)):
            '''一次打开self.num个个线程同时执行'''
            title.append(code[i][2]+code[i][1])
            t = threading.Thread(target=Short_Url,args={code[i],})
            threads.append(t)
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        return msg
#A=News("10")
#print A.run()


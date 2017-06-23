#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/20 0020 23:59
# @Author  : Labulaka
# @Mail     :labulaka521@live.cn
# @FileName    : itchat_api_news.py
'''未使用多线程'''
import urllib2,re,requests,json,time
new_url = "http://www.chinanews.com/scroll-news/news1.html"
def G_code(url):
    '''获取页面源码'''
    user_agent = {"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"}
    headers = {"User-Agent":user_agent}
    request = urllib2.Request(url,headers = headers)
    text = urllib2.urlopen(request).read()
    text = text.decode('gbk').encode('utf-8')
    return text
class News():
    '''
    获取最新新闻消息
    '''
    def __init__(self,num):
        '''num 是总共获取的新闻数量,默认为10'''
        if  num:
            self.num = num
        else:
            self.num = 10

    def Get_Link(self):
        '''得到标题和原始链接'''
        Link = []
        code = G_code(new_url)
        pattern = re.compile(r'<div class="dd_bt"><a href="//(.*?)">(.*?)</a></div>.*?<div class="dd_time">(.*?)</div>',re.S)
        for item in re.findall(pattern,code):
            if self.num > 0:
                Link.append(item)
            self.num = int(self.num) - 1
        #print len(Link)
        return Link
    def Short_Url(self,long_url):
        '''将长连接转化为新浪短链接'''
        url_api = "https://api.weibo.com/2/short_url/shorten.json"
        payload = {
            "source":5786724301,
            "url_long":long_url
        }
        r = requests.get(url_api,params=payload)
        text = json.loads(r.text)
        if text['urls'][0]["result"]:
            #print time.strftime("%M:%S",time.localtime(time.time()))
            return text['urls'][0]['url_short']
        else:
            return text['urls'][0]['url_short'],"已失效"
    def run(self):
        '''获取新闻标题及相应的短连接'''
        Code = []

        for item in News(self.num).Get_Link():
            #Code[item[2]+"\n"+item[1]+"\n"] = News(self.num).Short_Url("http://"+"\t"+item[0])
            Code.append((item[2]+item[1]+str(News(self.num).Short_Url("http://"+"\t"+item[0]))+"\n"))
        return Code
code = News("1")
print code.run()
# if __name__ == "__main__":
#     print "Error，此程序仅支持被导入，使用方法如下："
#     print '''
#         使用方法：
#             import new
#             code = new.News("num")
#             code.run()
#             "num" 此参数非必须，如没有则默认拉取10条最新新闻，如需更改数量则加上此参数
#         '''

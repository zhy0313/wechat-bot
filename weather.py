#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/19 0019 19:49
# @Author  : Labulaka
# @Mail     :labulaka521@live.cn
# @FileName    : weather.py

import json,requests,re,urllib2,json
import fileinput
key = "be155efb99b045e6880bd103008bc3e3"
class We():
    '''获取近三天的天气状况'''
    def __init__(self,city):
        self.city = city
        self.url = "https://free-api.heweather.com/v5/"
    def run(self):
        '''天气状况,使用now表示'''
        hourly_url = self.url+"weather"
        payload = {
            "city":self.city,
            "key":key
        }
        r = requests.get(hourly_url,params=payload)
        text = json.loads(r.text)
        if text["HeWeather5"][0]["status"] == "ok":
            #status_code = 0

            return text["HeWeather5"][0]
#A = We("西安")
#A.run()
# if __name__ == "__main__":
#     print "Error,此程序只可以导入，下面是使用方法"
#     print '''
#         import weather
#         A = weather.We("城市名称")
#         #城市名称格式: 西安,xian
#         A.run()
#         '''

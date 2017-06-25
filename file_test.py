#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 0022 9:43
# @Author  : Labulaka
# @Mail     :labulaka521@live.cn
# @FileName    : file_test.py
import re
# import requests
# import urllib2
# city_name = []
# text = urllib2.urlopen("https://cdn.heweather.com/china-city-list.txt").readlines()
# for i in text:
#     if re.search('CN',i):
#         city_name.append(re.split('\t',i)[0]+"\t"+re.split('\t',i)[9])
# f=open("city_list.txt","w")
# f.write('\n'.join(city_name))
# f.close()
city_list = []
i = 0
txt = open('city_list.txt').readlines()

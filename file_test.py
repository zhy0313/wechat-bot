#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 0022 9:43
# @Author  : Labulaka
# @Mail     :labulaka521@live.cn
# @FileName    : file_test.py
'''处理城市名称'''
import re
f=open("wechat_bot/china_city_list.txt","r").readlines()
f1=open("wechat_bot/china_city_list1.txt","w")
a= []
for item in f:
    b =re.split('\t',item)[9]+re.split('\t',item)[8]+"\n"
    if b  not in a:
        a.append(b)
        f1.write(b)
f1.close()


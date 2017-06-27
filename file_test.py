#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 0022 9:43
# @Author  : Labulaka
# @Mail     :labulaka521@live.cn
# @FileName    : file_test.py
import itchat
@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print msg['Text']
    print msg
    itchat.send("test",toUserName="filehelper")
itchat.auto_login()
itchat.run()

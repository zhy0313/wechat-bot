#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/20 0020 1:22
# @Author  : Labulaka
# @Mail     :labulaka521@live.cn
# @FileName    : weixin.py

import itchat,re,time
import new_thread,kuaidi,weather
def Type_m(m):
    '''判断用户输入的参数'''

    city_list = open('/home/labulaka/python/wechat_bot/city_list.txt',"r").read()
    new = [u"资讯",u"新闻",u"热点",u"快讯",u"身边事"]
    list = city_list
    for i in range(len(new)):
        if new[i] in m:
            return 1        #用户获取新闻的状态码
    if m in list:
        return 2           #用户获取天气的的状态码
    elif re.search(r"[0-9]{5,20}",m):
        return 3           #用户获取快递物流信息的状态码
    else:
        return 0            #不能识别用户所发信息的状态码
    city_list.close()

def reply_m(m):
    '''当状态码为1时，获取新闻消息'''

    try:
        pattern = re.compile(r'[0-9]{1,4}',re.S)
        num = re.findall(pattern,m['Text'])[0]
    except IndexError:
        num = 10
    if int(num) >= 100:
        itchat.send(u"你想累死我吗[委屈]，减少点新闻数量吧[愉快]",m['FromUserName'])
        return 1
    itchat.send(u"正在为您查询最新的新闻[愉快]，请稍等一会",m['FromUserName'])
    msg = new_thread.News(num).run()
    txt = []
    for item in msg:
        txt.append(item)
    itchat.send("".join(txt),m['FromUserName'])
    itchat.send(u"新闻已发送完成[困]，共发送出 %d 条\n获取新闻的格式: 新闻,新闻5\n(数字是获取新闻的数量，默认回复10条)" % len(msg),m['FromUserName'] )
def reply_w(m):
    '''当状态码为2时，调用次函数来获取天气状况'''
    city_list = open('/home/labulaka/python/wechat_bot/city_list.txt',"r").read()
    list = city_list
    for i in re.split('\n',list):
        if m['Text'] in i:
            city_code = re.split('\t',i)[0]
            break
    itchat.send(u"正在为您查询天气[愉快],请稍后...",m['FromUserName'])
    w = weather.We(city_code).run()
    if w == None:
        itchat.send(u"Oh[发怒]..你输入的地址我还难以确定是哪[委屈],请输入具体的城市名称",m['FromUserName'])
        return 0
    w_txt = []
    w_txt.append(u"%s实时天气状况[跳跳]\n\t\t\t更新时间:%s\n\t\t\t天气状况:%s\n\t\t\t气温:%s℃\n\t\t\t风力:%s\n" %\
                (w['basic']['city'],w['basic']['update']['loc'],w['now']['cond']['txt'],w['now']['tmp'], \
                 w['now']['wind']['sc']))
    #发送未来两天天气预报
    fmsg = w["daily_forecast"]
    for item in range(0, 2):
        w_txt.append(u"天气预报[转圈]\n\t\t\t时间:%s\n\t\t\t天气状况:白天:%s\t  晚上:%s\n\t\t\t气温范围:%s--%s℃\n\t\t\t风力:%s\n" % \
                    (fmsg[item]["date"],fmsg[item]["cond"]["txt_d"],fmsg[item]["cond"]["txt_n"], \
                     fmsg[item]["tmp"]["min"],fmsg[item]["tmp"]["max"],fmsg[item]["wind"]["sc"]))
    itchat.send("".join(w_txt),m['FromUserName'])
    itchat.send(u"%s的天气情况已经发送完成[困]"%(w['basic']['city']),m['FromUserName'])

def reply_k(m):
    '''当状态码为3时，用户发来的是快递单号，返回物流信息'''

    itchat.send(u"正在查询物流信息[愉快],请稍后...",m['FromUserName'])
    msg = kuaidi.Kuaidi(m['Text']).run()
    if msg== None:
        itchat.send(u"你输入的快递单号貌似我还没有收录进来的[难过]你再确认一下%s是否正确[皱眉]"%m['Text'],m['FromUserName'])
        return 0
    # if u"签收" not in ''.join(msg):
    #     kuaidi_again = u"\n------------------------------\n快递还未签收，当您的快递物流有更新时会为您再次发送最新最新物流信息"
    # else:
    #     kuaidi_again = ""
    itchat.send("\n".join(msg),m['FromUserName'])

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    if Type_m(msg['Text']) == 1:
         '''当状态码为1时，给用户发送新闻信息'''
         reply_m(msg)
    elif Type_m(msg['Text']) == 2: 
         reply_w(msg)
    elif Type_m(msg['Text']) == 3:
         reply_k(msg)
    elif msg['Text'] in [u"菜单",u"功能",u"你是谁",u"你是",u"用户",u"做什么"]:
         itchat.send(u"我叫小太阳[愉快]\
                    我可以为你查询\
                    天气情况(给我发送城市名称或者城市拼写),快递物流信息(给我发送快递单号),实时新闻,\
                    快来试试吧[害羞]",\
                     msg['FromUserName'])
    else:
         itchat.send(u"因为我有个笨主人[发怒]\
                    所以我还很笨[难过]\
                    还不能理解你是什么意思[委屈]\
                    现在的我只可以查询新闻,天气状况\还有快递物流信息[抠鼻]\
                    举个栗子你可以回复我:新闻5,来点新闻,西安,123456789",\
                       msg['FromUserName'])
@itchat.msg_register(itchat.content.FRIENDS)
def add_friend(msg):
    '''自动加好友'''
    if msg['RecommendInfo']['Content'] == "labulaka":
         msg.user.verify()
         msg.user.send(u"你好呀,我叫小太阳[愉快]\
                我可以为你查询天气情况(城市名称或者城市拼写),快递物流信息(快递单号),实时新闻,还可以回复菜单查看所有的功能\
                快来试试吧[害羞]")
         itchat.send(u"已经同意用户%s发来的添加好友请求" % msg['RecommendInfo']['NickName'],toUserName='@adef36898cb8c50daf6951bce09f6463')
    else:
         itchat.send(u"已经忽略用户%s发来的添加好友请求\n原因:没有输入指定验证信息" % msg['RecommendInfo']['NickName'],toUserName='@adef36898cb8c50daf6951bce09f6463')
itchat.auto_login(hotReload=True)
itchat.run()

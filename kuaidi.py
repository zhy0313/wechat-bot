#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/21 0021 1:51
# @Author  : Labulaka
# @Mail     :labulaka521@live.cn
# @FileName    : kuaidi.py

import json,requests,hashlib,base64
class Kuaidi():
    def __init__(self,LogisticCode):
        self.api = "http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx"   #快递鸟api调用地址
        self.key = "c0692e01-114d-4814-b438-7a9f2615649b"        #用户key
        self.EBusinessID = "1292649"         #用户io
        self.code = LogisticCode        #订单编号
    def Sign(self,requestdata):
        '''获取数字签字 MD5 base64加密key与requestdata'''
        m = hashlib.md5()
        RequestsData = requestdata+self.key
        m.update(RequestsData.encode('utf-8'))
        return base64.b64encode(str(m.hexdigest()).encode("ascii")).decode("ascii")
    def Shipper(self):
        '''获取订单编号所属快递公司'''
        RequestData = '{"LogisticCode":"' + self.code + '"}'
        DataSign = Kuaidi(self.code).Sign(RequestData)
        payload = {
            "DataSign":DataSign,
            "DataType":2,
            "EBusinessID":self.EBusinessID,
            "RequestData":RequestData,
            "RequestType":2002,
        }
        r = requests.get(self.api,params = payload)
        shipper = []
        for item in range(len(json.loads(r.text)["Shippers"])):
            shipper.append(json.loads(r.text)["Shippers"][item]["ShipperCode"])
        return shipper
    def run(self):
        '''获取物流信息'''
        #RequestsData = '{"LogisticCode":'+self.code+' ,"ShipperCode":Kuaidi(self.code).Shipper()}
        for item in range(len(Kuaidi(self.code).Shipper())):
            RequestsData = '{"LogisticCode":"' + self.code + '","ShipperCode":"' + Kuaidi(self.code).Shipper()[item] + '"}'
            DataSign = Kuaidi(self.code).Sign(RequestsData)
            payload = {
                "DataSign":DataSign,
                "DataType":2,
                "EBusinessID":self.EBusinessID,
                "RequestData": RequestsData,
                "RequestType": 1002
            }
            r = requests.get(self.api,params=payload)
            text = json.loads(r.text)
            item = len(text["Traces"])
            if item == 0:       #如果没有物流信息则直接返回
                break
            shipper = []
            for i in range(item):
                shipper.append(text["Traces"][i]["AcceptTime"]+"\n"\
                      +text["Traces"][i]["AcceptStation"])
            return shipper
#Get = Kuaidi("1000745320654")
#print(Get.run())
if __name__=="__main__":
    print("Error,此程序只可以导入，下面是使用方法")
    print('''
        import kuaidi
        Find = kuaidi.Kuaidi("订单编号")
        Find.run()
        ''')

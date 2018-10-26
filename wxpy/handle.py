# -*- coding: utf-8 -*-
import hashlib
import web
import time
from flask import Flask, request, make_response
import hashlib
import json
import xml.etree.ElementTree as ET

from dispatcher import *


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "weixin" # 请按照公众平台官网\基本配置中信息填写
            my_list = [token, timestamp, nonce]
            my_list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update,  my_list)
            hashcode = sha1.hexdigest()
            list1 = [token, timestamp, nonce]
            list1.sort()
            str_list1 = ''.join(list1)
            sha2 = hashlib.sha1()
            sha2.update(str_list1.encode('utf-8'))
            hashcode2 = sha2.hexdigest()
            print("handle/GET func: hashcode, signature, hashcode2: ", hashcode, signature, hashcode2)
            if hashcode2 == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        rec = request.stream.read()  # 接收消息
        dispatcher = MsgDispatcher(rec)
        data = dispatcher.dispatch()
        with open("./debug.log", "a") as file:
            file.write(data)
            file.close()
        response = make_response(data)
        response.content_type = 'application/xml'
        return response


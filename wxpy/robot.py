#!/usr/bin python
#coding: utf8
import requests
import json

def get_turing_response(req=""):
    url = "http://www.tuling123.com/openapi/api"
    secretcode = "7cc0c37863e54801a850b145c76cfae5"
    response = requests.post(url=url, json={"key": secretcode, "info": req, "userid": 12345678})
    return json.loads(response.text)['text'] if response.status_code == 200 else ""

def get_qingyunke_response(req=""):
    url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg={}".format(req)
    response = requests.get(url=url)
    return json.loads(response.text)['content'] if response.status_code == 200 else ""

# 简单做下。后面慢慢来
def get_response_by_keyword(keyword):
    if '团建' in keyword:
        result = {"type": "image", "content": "3s9Dh5rYdP9QruoJ_M6tIYDnxLLdsQNCMxkY0L2FMi6HhMlNPlkA1-50xaE_imL7"}
    elif 'music' in keyword or '音乐' in keyword:
        musicurl='http://fs.w.kugou.com/201810261426/6498a31690479bd9f3b7ac5a9aa6b1cb/G016/M0A/1C/19/UA0DAFU2KnaAKjtdADfQcvsyA40286.mp3'
        result = {"type": "music", "content": {"title": "80000", "description":"有个男歌手姓巴，他的女朋友姓万，于是这首歌叫80000", "url": musicurl, "hqurl": musicurl}}
    elif '关于' in keyword:
        items = [{"title": "关于我", "description":"喜欢瞎搞一些脚本", "picurl":"https://avatars1.githubusercontent.com/u/12973402?s=460&v=4", "url":"https://github.com/guoruibiao"},
                 {"title": "我的博客", "description":"收集到的，瞎写的一些博客", "picurl":"http://avatar.csdn.net/0/8/F/1_marksinoberg.jpg", "url":"http://blog.csdn.net/marksinoberg"},
                 {"title": "薛定谔的��", "description": "副标题有点奇怪，不知道要怎么设置比较好","picurl": "https://www.baidu.com/img/bd_logo1.png","url": "http://www.baidu.com"}
                 ]
        result = {"type": "news", "content": items}
    else:
        result = {"type": "text", "content": "可以自由进行拓展"}
    return result

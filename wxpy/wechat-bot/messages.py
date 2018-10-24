# -*- coding: utf-8 -*-

import io
import requests
from lxml import etree
import json
import random
import apiai
from bs4 import BeautifulSoup
import urllib
from api_tokens import *
import time
time1 = time.time()
from PIL import Image
import pytesseract
from PIL import ImageEnhance

def tuling_reply(msg_content, user_id):
    url_api = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': TULING_TOKEN,
        'info': msg_content,
        'userid': user_id,
    }

    print("use Tuling reply")
    s = requests.post(url_api, data=data).json()
    print(s)
    print('return code: ' + str(s['code']))
    if s['code'] == 100000:
        return s['text']
    if s['code'] == 200000:
        return s['text'] + s['url']
    if s['code'] == 302000:
        news = random.choice(s['list'])
        return news['article'] + '\n' + news['detailurl']
    if s['code'] == 308000:
        menu = random.choice(s['list'])
        return menu['name'] + '\n' + menu['detailurl'] + '\n' + menu['info']


def apiai_reply(msg_content, user_id):
    print("try APIAI reply...")
    ai = apiai.ApiAI(APIAI_TOKEN)
    request = ai.text_request()
    request.lang = 'zh-CN'
    request.session_id = user_id
    request.query = msg_content

    response = request.getresponse()
    s = json.loads(response.read().decode('utf-8'))

    if s['result']['action'] == 'input.unknown':
        raise Exception('api.ai cannot reply this message')
    if s['status']['code'] == 200:
        print("use APIAI reply")
        print('return code: ' + str(s['status']['code']))
        return s['result']['fulfillment']['speech']


def emotions_reply(keyword):
    print("try gif reply...")

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.example.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}

    url = 'https://www.doutula.com/search?keyword=' + str(keyword)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    img_src = soup.find('div', attrs={'class':'random_picture'}).find_all('a', attrs={'class':'col-xs-6 col-md-2'})
    res = ''
    if len(img_src) > 0:
        res = random.choice(img_src).find('img').get('data-original')
    return res

###########二值化算法
def binarizing(img,threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


###########去除干扰线算法
def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img


########身份证号码识别
def identity_OCR(pic_path):
    #####身份证号码截图
    img1 = Image.open(pic_path)
    w, h = img1.size
    ##将身份证放大3倍
    out = img1.resize((w * 3, h * 3), Image.ANTIALIAS)
    region = (125 * 3, 200 * 3, 370 * 3, 250 * 3)
    # 裁切身份证号码图片
    cropImg = out.crop(region)
    # 转化为灰度图
    img = cropImg.convert('L')
    # 把图片变成二值图像。
    img1 = binarizing(img, 100)
    img2 = depoint(img)
    code = pytesseract.image_to_string(img2)
    print(code)
    print("识别该身份证号码是:" + str(code))
    im = Image.open('5.png')
    enhancer = ImageEnhance.Color(im)
    enhancer = enhancer.enhance(0)
    enhancer = ImageEnhance.Brightness(enhancer)
    enhancer = enhancer.enhance(2)
    enhancer = ImageEnhance.Contrast(enhancer)
    enhancer = enhancer.enhance(8)
    enhancer = ImageEnhance.Sharpness(enhancer)
    im = enhancer.enhance(20)
    print(pytesseract.image_to_string(im))

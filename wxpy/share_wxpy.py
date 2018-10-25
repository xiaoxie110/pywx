#!/usr/bin/python3
# coding=utf-8
from wxpy import *
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(curPath)
print(curPath)
#####from messages import *
from wxpy import get_wechat_logger
import unicodedata
import re
import time
import logging
import threading
from tempfile import NamedTemporaryFile
from xml.etree import ElementTree as ETree
from html.parser import HTMLParser

bot = Bot(cache_path=True,console_qr=True)

# 机器人账号自身
myself = bot.self

# # 向文件传输助手发送消息
# bot.file_helper.send('Hello from wxpy!')

# 启用 puid 属性，并指定 puid 所需的映射数据保存/载入路径
bot.enable_puid('wxpy_puid.pkl')


# 注册好友请求类消息
@bot.register(msg_types=FRIENDS)
# 自动接受验证信息中包含 'python' 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    if 'python' in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('你好，我是python机器人，接收一下指令哦：\n'
                        '**天气\n'
                        '**酒店\n')


# 指定一个好友
print(bot.friends())
my_friend = bot.friends().search('python')[0]
print(bot.friends().stats_text(total=True, sex=True))

# 简单基本聊天
tuling = Tuling(api_key='7cc0c37863e54801a850b145c76cfae5')
extensions = ['.jpg', '.png', '.gif']
# 图灵机器人手动消息
def talks_robot(info='Husen'):
    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = '7cc0c37863e54801a850b145c76cfae5'
    data = {'key': apikey, 'info': info}
    req = requests.post(api_url, data=data).text
    replys = json.loads(req)
    return replys

@bot.register(my_friend)
def reply(msg):
    content = re.sub('@[^\s]*', '', unicodedata.normalize('NFKC', msg.text)).strip()
    if content.endswith(tuple(extensions)):
        try:
            res = requests.get(emotions_reply(content[:-4]), allow_redirects=False)
            tmp = NamedTemporaryFile(delete=False)
            tmp.write(res.content)
            tmp.flush()
            try:
                # 发送图片
                media_id = bot.upload_file(tmp.name)
                tmp.close()
                msg.reply_image('.gif', media_id=media_id)
            except ResponseError as e:
                # 抛出异常
                print(e.err_code, e.err_msg)  # 查看错误号和错误消息
        except Exception as error:
            print(error)
            msg.reply("本机器人没有找到相关表情~使用文字回复：\n" + tuling.do_reply(msg))
    else:
        # print(talks_robot(info=msg.text))
        print(msg.raw)
        tuling.do_reply(msg)
        print(getattr(msg.chat, 'province', None))


# group_3 = bot.groups().search('xoxoxo')[0]
#
#
# @bot.register(group_3)
# def invite(user):
#     if user in group_3:
#         user.send('你已加入 {}'.format(group_3.nick_name))
#     else:
#         try:
#             group_3.add(user, use_invitation=False)
#         except ResponseError as e:
#             # 抛出异常
#             print(e)
#             print(e.err_code, e.err_msg)  # 查看错误号和错误消息
#
#
# # 验证入群口令
# def valid(msg):
#     return 'wechat' in msg.text.lower()
#
#
# # 响应好友消息
# # @bot.register(my_friend, msg_types=TEXT)
# # def exist_friends(msg):
# #     if valid(msg):
# #         invite(msg.sender)
# #     else:
# #         tuling.do_reply(msg)
#
# # 针对测回的消息发送要助手
# @bot.register([my_friend, group_3], msg_types=NOTE)
# def get_revoked(msg):
#     # 检查 NOTE 中是否有撤回信息
#     msgStr = HTMLParser().unescape(msg.raw['Content'])
#     try:
#         revoked = ETree.fromstring(msgStr).find('revokemsg')
#         if revoked:
#             # 根据找到的撤回消息 id 找到 bot.messages 中的原消息
#             revoked_msg = bot.messages.search(id=int(revoked.find('msgid').text))[0]
#             # 原发送者 (群聊时为群员)
#             sender = msg.member or msg.sender
#             # 把消息转发到文件传输助手
#             revoked_msg.forward(
#                 bot.file_helper,
#                 prefix='{} 撤回了:'.format(sender.name)
#             )
#     except ResponseError as e:
#         # 抛出异常
#         print(e.err_code, e.err_msg)  # 查看错误号和错误消息
#
#
# # 新人欢迎消息
# def welcome(msg):
#     welcome_text = '''******\U0001F389\U0001F389\U0001F389\U0001F389******\n
#      欢迎 @{} 加入本群！\n\n*******************************'''
#     try:
#         new_member_name = re.search(r'邀请"(.+?)"|"(.+?)"通过', msg.text).group(1)
#     except AttributeError:
#         return
#
#     return welcome_text.format(new_member_name)
#
#
# girl_friend = bot.friends().search('秀秀')[0]
#
# #响应女朋友消息
# # @bot.register(girl_friend)
# # def reply(msg):
# #     print(msg)
# #     msg.forward(my_friend)
# #
# # @bot.register(my_friend)
# # def reply(msg):
# #     print(msg)
# #     msg.forward(girl_friend)
#
# card_msg = None
# no_card_notice = '名片尚未确认，请手动发送到文件传输助手'
#
#
# # 第一步: 手动向自己的文件传输助手发送一次所需的名片
# @bot.register(bot.file_helper, CARD, except_self=False)
# def get_card_msg_to_send(msg):
#     global card_msg
#     logging.info('获得了名片: {}'.format(msg.card.name))
#     card_msg = msg
#
# #整点报时
# while 1:
#     hour = time.strftime('%H', time.localtime(time.time()))
#     minutes = time.strftime('%M', time.localtime(time.time()))
#     seconds = time.strftime('%S', time.localtime(time.time()))
#
#     if (hour == '07' and minutes == '30' and seconds == '00'):
#         nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#         group_3.send('早上好！\n起床啦，为您整点报时：\n{}\n--------今日天气--------\n{}'.format(nowTime,talks_robot(info='深证市福田区天气')))
#     elif(hour == '12' and minutes == '00' and seconds == '00'):
#         nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         girl_friend.send('中午好！\n该吃饭了，为你整点报时：\n{}\n--------轻松一下--------\n{}'.format(nowTime,talks_robot(info='讲个笑话')))
#     elif (hour == '13' and minutes == '30' and seconds == '00'):
#         nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         group_3.send('下午好！\n该干活了，为您整点报时：\n{}\n--------轻松一下--------\n{}'.format(nowTime, talks_robot(info='讲个笑话')))
#     elif (hour == '00' and minutes == '00' and seconds == '00'):
#         nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         group_3.send('晚上好！\nIt\'s 宵夜time，为您整点报时：\n{}\n--------晚安全世界--------'.format(nowTime))
#
#     time.sleep(1)
#
#
embed()

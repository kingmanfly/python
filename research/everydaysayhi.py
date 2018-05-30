from __future__ import unicode_literals
from threading import Timer
from wxpy import *  #wxpy 在 itchat 的基础上，通过大量接口优化提升了模块的易用性，并进行丰富的功能扩展。
import requests

bot=Bot()

def get_news1():
    #获取金山词霸每日一句，英文和翻译
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    contents = r.json()['content']
    translation= r.json()['translation']
    return contents,translation

def send_news(): 
    try:
        my_friend = bot.friends().search(u'大学同学上海')[0]
        #你朋友的微信名称，不是备注，也不是微信帐号。       
        my_friend.send(get_news1()[0])
        my_friend.send(u"每一分钟发一次")
        t = Timer(60, send_news)
        #每86400秒（1天），发送1次，不用linux的定时任务是因为每次登陆都需要扫描二维码登陆，很麻烦的一件事，就让他一直挂着吧   
        t.start()
    except:
        my_friend = bot.friends().search('努力，奋斗')[0]
        #你的微信名称，不是微信帐号。
        my_friend.send(u"今天消息发送失败了")

def send_group_news(): 
    try:
        # 需要将群组保存在通讯录才可见
        my_group = bot.groups().search(u'大学同学上海')[0]
        #你朋友的微信名称，不是备注，也不是微信帐号。       
        my_group.send(get_news1()[0])
        my_group.send(u"每一分钟发一次")
        t = Timer(60, send_group_news)
        #每86400秒（1天），发送1次，不用linux的定时任务是因为每次登陆都需要扫描二维码登陆，很麻烦的一件事，就让他一直挂着吧   
        t.start()
    except:
        my_friend = bot.friends().search('努力，奋斗')[0]
        #你的微信名称，不是微信帐号。
        my_friend.send(u"今天消息发送失败了")
if __name__ == "__main__":
    # send_news()
    send_group_news()
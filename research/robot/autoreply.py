import sys
import requests
import itchat, time
import random

if len(sys.argv) > 1:
    filter_key = sys.argv[1]
else:
    filter_key = '人工智能'

KEY = '45bb4559dabf43b4be9d3d4a934cc20b'
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data = data).json()
        return r.get('text')
    except:
        return

@itchat.msg_register(itchat.content.TEXT,isFriendChat=True, isGroupChat=True, isMpChat=True)
def tuling_reply(msg):
    robots = ['--机器人A','--机器人B']
    
    # 群聊@
    if msg.isAt:
        itchat.send_msg(u'有人在"%s"群里@了你, %s\u2005说: %s'%(
                msg['User']['NickName'], 
                msg.actualNickName,
                msg.text), 
            'filehelper')

    # 群聊 关键字
    if msg.FromUserName.find('@@') == 0:
        
        if msg.Text.find(filter_key) != -1:
            itchat.send_msg(u'可能你感兴趣|"%s"群里, "%s"说:"%s"'%(
                    msg['User']['NickName'], 
                    msg['ActualNickName'], 
                    msg['Content']), 
                'filehelper') 
    
    """ # 私信    
    if msg['Text'].find('你太笨了') != -1:
        # u/U:表示unicode字符串
        itchat.send_msg(u'有人骂你,"%s"说:"%s"'%(
            msg['User']['NickName'], msg['Content']), 'filehelper')
 """
    # 过滤群
    # if msg['User']['NickName'] == '大学同学上海':
    #     reply = get_response(msg['Text']) + random.choice(robots)
    #     return reply

itchat.auto_login(hotReload = True)
itchat.run()
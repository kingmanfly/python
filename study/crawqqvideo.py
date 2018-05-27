from urllib import request
from http import cookiejar
from urllib import error
import re
import time

# 视频编号
vid = '2470886964'

# 评论起始编号
comid = '0'

url = "http://coral.qq.com/article/" + vid + "/comment?commentid=" + comid + "&reqnum=20"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # Accept-Encoding: gzip, deflate #最好不要写或者写成Accept-Encoding: utf-8,gb2312
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36",
    "Connection": "keep-alive",     #或者"Proxy-Connection": "keep-alive"
    "referer":"qq.com"  #一般为它的首页
}
cjar = cookiejar.CookieJar()
proxy = request.ProxyHandler({'http':'127.0.0.1:8888'})    #为Fiddler截获调试用
opener = request.build_opener(proxy, request.HTTPHandler, request.HTTPCookieProcessor(cjar))

headall = []
for key,value in headers.items():
    item = (key,value)
    headall.append(item)
opener.addheaders = headall
request.install_opener(opener)

# 建立自定义函数，实现自动爬取对应评论网页并返回爬取内容
def craw(vid, comid):
    url = "http://coral.qq.com/article/" + vid + "/comment?commentid=" + comid + "&reqnum=20"
    try:
        data = request.urlopen(url).read().decode('utf-8')
        return data
    except error.HTTPError as e:
        print(e.code)
        print(e.reason)
        time.sleep(10)
    except error.URLError as e:
        print(e.reason)
        time.sleep(10)
    except Exception as e:
        time.sleep(1)

# 爬取该网页
idpat = '"id":"(.*?)"'
userpat = '"nick":"(.*?)"'
contentpat = '"content":"(.*?)"'

for i in range(1, 10):
    print("---------------------------------")
    print("第" + str(i) + "页评论内容")
    data = craw(vid, comid)
    if data == None:
        continue
    else:
        idlist = re.findall(idpat, data, re.S)
        userlist = re.findall(userpat, data, re.S)
        contentlist = re.findall(contentpat, data, re.S)
        for i in range(0, len(idlist)):
            print("用户名是："+ eval('u"'+ userlist[i]+'"'))
            try:
                print("评论内容是："+ eval('u"'+ contentlist[i]+'"'))
            except Exception as e:
                print("解析异常")
            print("\n")
        if idlist != []:
            comid = idlist[len(idlist) - 1]
        else:
            break


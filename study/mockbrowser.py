from urllib import request
from http import cookiejar

url = "http://news.163.com/16/0825/09/BVA8A9U500014SEH.html"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # Accept-Encoding: gzip, deflate #最好不要写或者写成Accept-Encoding: utf-8,gb2312
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36",
    "Proxy-Connection": "keep-alive", #或者"Connection": "keep-alive"
    "referer":"http://www.163.com/" #一般为他的首页
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
data = request.urlopen(url).read()
fhandle = open('D:/training/python/13.html', 'wb')
fhandle.write(data)
fhandle.close()

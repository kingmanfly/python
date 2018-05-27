import re
from urllib import request

def getlink(url):
    req = request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
    r = request.urlopen(req)
    data = r.read()

    link_pattern = '(https?://[^\s");]+\.(\w|/)*)'
    link = re.findall(link_pattern, str(data))
    link = list(set(link))
    return link

url = 'https://blog.csdn.net/'
linklist = getlink(url)
for link in linklist:
    #(https?://[^\s");]+\.(\w|/)*)这个模式最外面的括号是整体链接，位于位置0，里面的(\w|/)位于位置1
    print(link[0]) 
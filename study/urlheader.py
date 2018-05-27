from urllib import request

url = 'https://blog.csdn.net/weiwei_pig/article/details/51178226'
# headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
# opener = request.build_opener()
# opener.addheaders = [headers]
# r = opener.open(url)

req = request.Request(url)
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
r = request.urlopen(req)
data = r.read()

print(str(data, encoding='utf-8'))

fhandle = open('D:/training/python/3.html', 'wb')
fhandle.write(data)
fhandle.close()
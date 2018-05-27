from urllib import request
from urllib import parse

url = 'http://www.test.com/api/postdata/'
post_data = parse.urlencode({
    "name":"kingman@infosys.com",
    "password":"123456"
}).encode('utf-8')
req  = request.Request(url, post_data)
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
data = request.urlopen(req).read()

print(str(data, encoding='utf-8'))

fhandle = open('D:/training/python/4.html', 'wb')
fhandle.write(data)
fhandle.close()
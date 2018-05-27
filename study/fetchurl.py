from urllib import request
r = request.urlopen('http://www.baidu.com')

data = r.read()

fhandle = open('D:/training/python/1.html', 'wb')
fhandle.write(data)
fhandle.close()
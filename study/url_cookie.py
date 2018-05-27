from urllib import request
from urllib import parse
from http import cookiejar

url = 'http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=Lh3j7'

# 打包post参数
post_data = parse.urlencode({
    "username":"kingmanfly",
    "password":"kingman_li"
}).encode('utf-8')
req  = request.Request(url, post_data)

# 增加表头
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")

# 创建CookieJar对象
cjar = cookiejar.CookieJar()

# 使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
opener = request.build_opener(request.HTTPCookieProcessor(cjar))

# 将opener安装为全局
request.install_opener(opener)

# 用opener来访问Request
file = opener.open(req)
data = file.read()

# 写入到文件
fhandle = open('D:/training/python/6.html', 'wb')
fhandle.write(data)
fhandle.close()

#接着爬取数据
url2 = 'http://bbs.chinaunix.net'
req2  = request.Request(url2, post_data)
req2.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")

# 使用request访问请求
data2 = request.urlopen(req2).read()
fhandle = open('D:/training/python/7.html', 'wb')
fhandle.write(data2)
fhandle.close()

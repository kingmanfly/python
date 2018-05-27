import re
from urllib import request
from urllib import error
import time

# 模拟浏览器
headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
opener = request.build_opener()
opener.addheaders = [headers]

# 将opener安装为全局
request.install_opener(opener)

# 设置一列表listurl存储文章网址列表
listurl = []

# 自定义函数，使用代理功能
def use_proxy(proxy_addr, url):
    try:
        proxy = request.ProxyHandler({'http' : proxy_addr})
        # opener = request.build_opener(proxy, request.HTTPHandler)
        opener = request.build_opener()
        request.install_opener(opener)
        data = request.urlopen(url).read().decode('utf-8')
        return data
    except error.URLError as e:
        if hasattr(e, "reason"):
            print(e.reason)
        # 若为URLError异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        print('excetion:' + str(e))
         # 若为Exception异常，延时10秒执行
        time.sleep(1)

# 获取所有文章链接
def getlisturl(key, pagestart, pageend, proxy):
    try:
        page = pagestart

        # 编码关键字key
        keycode = request.quote(key)
        
        # 编码&page
        pagecode = request.quote('&page=')

        # 循环爬取各页的文章链接
        for page in range(pagestart, pageend):
            # 分别构建各页的url链接，每次循环构建一次
            # http://weixin.sogou.com/weixin?type=2&query=%E7%89%A9%E8%81%94%E7%BD%91&page=1
            url = "http://weixin.sogou.com/weixin?type=2&query=" + keycode + pagecode + str(page)
            data = use_proxy(proxy, url)

            # 获取文章链接的正则表达式
            listurpattern = '<div class="txt-box">.*?(http://.*?)"'
            # 获取每页的搜友文章链接并添加到列表listurl中
            listurl.append(re.findall(listurpattern, data, re.S))
        print("共获取到" + str(len(listurl)) + "页")
        return listurl
    except error.URLError as e:
        if hasattr(e, "reason"):
            print(e.reason)
        # 若为URLError异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        print('excetion:' + str(e))
         # 若为Exception异常，延时10秒执行
        time.sleep(1)

# 通过文件链接获取对应内容
def getcontent(listurl, proxy):
    i = 0

    # 本地文件中的html开头
    html1 = '''<!DOCTYPE html PUBLIC "=//w3c//DTD XHTML 1.0 Transitional//EN" "http://
        www.w3.org/TR/xhtm1/DTD/xhtml1-transitional.dtd>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>微信文章页面</title>
    </head>
    <body>'''
    fh = open('D:/training/python/8.html', 'wb')
    fh.write(html1.encode('utf-8'))
    fh.close()

    # 再次以追加写入的方式打开文件，以写入对应文章内容
    fh = open('D:/training/python/8.html', 'ab')
    # 此时listurl为二维列表，第一纬存储的信息跟页数相关，第二维存的跟该页链接有关
    for i in range (0, len(listurl)):
        for j in range(0, len(listurl[i])):
            try:
                url = listurl[i][j]
                # 处理成真实的url，分析发现采集网址比真实网址多了一串amp;
                url = url.replace("amp;", "")
                # 使用代理去爬取对应网址的内容
                data = use_proxy(proxy, url)

                # 文章标题正则表达式
                titlepat = "<title>(.*?)</title>"
                # 文章内容正则表达式
                contentpat = '(<div id="img-content">.*?)<ul id="js_hotspot_area"'

                title = re.findall(titlepat, data, re.S)
                content = re.findall(contentpat, data, re.S)

                thistitle = "此次没有获取到"
                thiscontent = "此次没有获取到"

                # 如果标题列表不为空，说明找到了标题，取列表第一个元素，即此次标题赋值给thistitle
                if(title != []):
                    thistitle = title[0]
                if(content != []):
                    thiscontent = content[0]

                # 将标题和内容汇总赋给变量dataall
                dataall="第" + str(i+1) + "页 第 " + str(j+1) + " 条 " + "<p>标题为: " + thistitle + "</p><p>内容为：" + thiscontent + "</p><br>"
                fh.write(dataall.encode('utf-8'))
                print("第 " + str(i) + " 个网页第" + str(j) + " 次处理")
            except error.URLError as e:
                if hasattr(e, "reason"):
                    print(e.reason)
                # 若为URLError异常，延时10秒执行
                time.sleep(10)
            except Exception as e:
                print('excetion:' + str(e))
                # 若为Exception异常，延时10秒执行
                time.sleep(1)
    fh.close()
    # 设置并写入到本地文件的html后面的部分
    html2 = '''</body>
</html>
    '''
    fh = open('D:/training/python/8.html', 'ab')
    fh.write(html2.encode('utf-8'))
    fh.close()

key = '闵行区小学排名'
proxy = '114.226.105.24:6666'   #暂时没有用代理，因为代理无法获取到数据

pagestart = 1
pageend = 4

listurl = getlisturl(key, pagestart, pageend, proxy)
print(len(listurl))
getcontent(listurl, proxy)


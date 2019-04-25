from urllib import request
from urllib import parse
from urllib import error
from http import cookiejar
import re
import time
import datetime
import json
import sys
import os
import requests

# 要获取的视频地址
videourl = 'http://www.iqiyi.com/v_19rrel12t4.html' #21克拉
videourl1 = 'http://www.iqiyi.com/v_19rrlhpgbg.html' #冰雪奇缘
videourl2 = 'http://www.iqiyi.com/v_19rrbrpwok.html#vfrm=2-4-0-1' #白雪公主
videourl3 = 'http://www.iqiyi.com/v_19rr7plwdc.html' # 红海行动
videourl4 = 'http://www.iqiyi.com/v_19rr7pe5k4.html'   #芳华
# 解析vip的网址
# 步骤一、get的url
get_master_url = 'http://y.mt2t.com/lines/'
# 步骤二、post这个url
post_master_url = 'http://y.mt2t.com/lines/urls/'

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "utf-8,gb2312",   #Accept-Encoding: gzip, deflate #最好不要写或者写成Accept-Encoding: utf-8,gb2312
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36",
    "Connection": "keep-alive",     #或者"Proxy-Connection": "keep-alive"
    "referer":"y2.xsdd.org"  #一般为它的首页
}
# 创建CookieJar对象
cjar = cookiejar.CookieJar()
proxy = request.ProxyHandler({'http':'117.36.103.170:8118'})    #为Fiddler截获调试用
opener = request.build_opener(request.HTTPHandler(debuglevel=0),request.HTTPSHandler(debuglevel=0), request.HTTPCookieProcessor(cjar))

# 增加头信息
headall = []
for key,value in headers.items():
    item = (key,value)
    headall.append(item)
opener.addheaders = headall

# 将opener安装为全局
request.install_opener(opener)

# 步骤一、自动选择线路
def get_parsed_url(ori_url):
    url = get_master_url + '?url=' + ori_url
    print(url)
    data = request.urlopen(url).read().decode('utf-8')
    return data

# 步骤二、自动选择线路
def post_parsed_url(ori_url):
    post_data = parse.urlencode({
        "url":ori_url,
        "type":""
    }).encode('utf-8')
    data = request.urlopen(post_master_url, post_data).read().decode('utf-8')
    print(data)
    return data

def pre_fetch_real_data(jsdata):
    data = request.urlopen(jsdata['Moren']).read().decode('utf-8')

def fetch_real_data(jsondata):
    base_url = 'http://y2.xsdd.org:91/ifr/api'
    moren = jsondata['Moren']

    url_pat = '.*url=(.*)&.*'
    type_pat = '.*type=(.*)'
    
    post_data = parse.urlencode({
        "url":  request.unquote(re.findall(url_pat, moren)[0]),
        "type": re.findall(type_pat, moren)[0],
        "from": "mt2t.com",
        "device":"",
        "up":0
    }).encode('utf-8')

    data = request.urlopen(base_url, post_data).read().decode('utf-8')
    ret_url_pat = '"url":"(.*?)"'
    result = re.findall(ret_url_pat, data)[0]
    return result

def download(url):
    print(url)
    new_url = ''
    now = datetime.datetime.now()
    
    download_path = os.getcwd() + "/" + now.strftime('%Y%m%d%H%M%S')
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    all_content = requests.get(url).text  # 获取M3U8的文件内容
    # all_content = request.urlopen(url).read().decode('utf-8') # 获取M3U8的文件内容
    file_line = all_content.splitlines()  # 读取文件里的每一行

    # 每家拼接方式不一样的，比如乐视是
    '''
    https://cdn.letv-cdn.com/20180430/smshC8Vz/index.m3u8
    指向内容：
        #EXTM3U
        #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1000000,RESOLUTION=1280x536
        /ppvod/E15650DF8B64364D61ED6112CE045E05.m3u8
    实际的m3u8为https://cdn.letv-cdn.com/ppvod/E15650DF8B64364D61ED6112CE045E05.m3u8
    下载地址：https://cdn.letv-cdn.com/20180430/smshC8Vz/1000kb/hls/a1APgIK2671000.ts
    '''
    # 每家拼接方式不一样的，比如优酷-土豆是
    '''
    http://youku.cdn-tudou.com/20180509/5830_9bd173fc/index.m3u8
    指向内容：
        #EXTM3U
        #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=800000,RESOLUTION=1080x608
        1000k/hls/index.m3u8
    实际的m3u8为http://youku.cdn-tudou.com/20180509/5830_9bd173fc/1000k/hls/index.m3u8
    '''
    if all_content.find('m3u8') != -1:
        print('子m3u8文件')
        oldwords_pat = '.*(/.*)'
        old_words = re.findall(oldwords_pat, url)[0]
        newwords_pat = '\s\S*\n(.*)'
        newwords = re.findall(newwords_pat, all_content)[0]
        new_url = url.replace(old_words, newwords)
        print("pass1" + new_url)
        sub_all_content = requests.get(new_url).text
        # all_content = request.urlopen(new_url).read().decode('utf-8') # 获取M3U8的文件内容
        file_line = sub_all_content.splitlines()  # 读取文件里的每一行

        # 换一种拼接方式
        if file_line[0] != "#EXTM3U":
            print('换一种拼接方式')
            oldwords_pat = 'https://.*?/(.*)'
            old_words = re.findall(oldwords_pat, url)[0]
            print(old_words)
            newwords_pat = '.*?/(.*.m3u8).*'
            newwords = re.findall(newwords_pat, all_content)[0]
            print(all_content)
            print("newwords " + newwords)
            new_url = url.replace(old_words, newwords)
            print(new_url)
            all_content = requests.get(new_url).text
            # all_content = request.urlopen(new_url).read().decode('utf-8') # 获取M3U8的文件内容
            file_line = all_content.splitlines()  # 读取文件里的每一行
    # 通过判断文件头来确定是否是M3U8文件
    if file_line[0] != "#EXTM3U":
        raise BaseException(u"非M3U8的链接")
    else:
        # 判断有无子m3u8文件
        unknow = True  # 用来判断是否找到了下载的地址
        print(new_url)
        for index, line in enumerate(file_line):
            if "EXTINF" in line:
                unknow = False
                # 拼出ts片段的URL
                c_fule_name = str(file_line[index + 1])
                c_fule_name_new = c_fule_name
                if new_url.find('letv'):
                    oldwords_pat = 'https://.*?/(.*)'
                    fule_pat = '.*/(.*)'
                    c_fule_name_new = re.findall(fule_pat, c_fule_name)[0]
                else:
                    oldwords_pat = '.*/(.*)'
                old_words = re.findall(oldwords_pat, new_url)[0]
                download_url = new_url.replace(old_words, c_fule_name)
                local_name = download_path + "/" + c_fule_name_new
                print("download_url = " + download_url)
                print("local_name = " + local_name)
                request.urlretrieve(url=download_url,filename=local_name)
        if unknow:
            raise BaseException("未找到对应的下载链接")
        else:
            print(u"下载完成")

get_parsed_url(videourl)
# time.sleep( 10 )
jsdata = json.loads(post_parsed_url(videourl))

# pre_fetch_real_data(jsdata)

download(fetch_real_data(jsdata))
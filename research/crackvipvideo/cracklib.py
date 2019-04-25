from urllib import request
from urllib import parse
from urllib import error
from http import cookiejar
import re
import time
import sys
import os
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
debug = True
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

class ParseVideoUrl():
    crack_base_url = 'http://y.mt2t.com'

    def __init__(self, url):
        if(debug):
            print('todo parse url is ' + url)
        self.url = url

    def prepare_line(self):
        url = ParseVideoUrl.crack_base_url + '/lines?url=' + self.url
        if(debug):
            print('prepare_line url is ' + url)
        data = request.urlopen(url).read().decode('utf-8')
        return data

    def load_real_url(self):
        post_data = parse.urlencode({
            "url":self.url,
            "type":""
        }).encode('utf-8')
        url = ParseVideoUrl.crack_base_url + "/lines/urls"
        data = request.urlopen(url, post_data).read().decode('utf-8')
        if(debug):
            print('prepare_line url is ' + url)
        return data

    def prepare_load_goal_url(self, jsdata):
        request.urlopen(jsdata['Moren']).read().decode('utf-8')
    
    def load_goal_url(self, jsondata):
        moren = jsondata['Moren']
        if(debug):
            print('moren is ' + moren)
        url_pat = '(http[s]?://.*?)\?'
        param_url_pat = '.*url=(.*)&.*'
        param_type_pat = '.*type=(.*)'
        
        post_data = parse.urlencode({
            "url":  request.unquote(re.findall(param_url_pat, moren)[0]),
            "type": re.findall(param_type_pat, moren)[0],
            "from": "mt2t.com",
            "device":"",
            "up":0
        }).encode('utf-8')
        request_url = re.findall(url_pat, moren)[0]
        data = request.urlopen(request_url + '/api', post_data).read().decode('utf-8')
        ret_url_pat = '"url":"(.*?)"'
        result = re.findall(ret_url_pat, data)[0]
        return result

class DownloadResourse():
    def __init__(self):
        pass

    def download(self, url, download_path):
        new_url = ''
        if(debug):
            print('download url is ' + url)
            print('local path is ' + download_path)
        if not os.path.exists(download_path):
            os.makedirs(download_path) # python创建多层目录的方式
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
            if(debug):
                print('有子m3u8文件')
            if url.find('youku.cdn-tudou.com') != -1:
                if(debug):
                    print('from youku.cdn-tudou.com')
                oldwords_pat = '.*/(.*)'
                old_words = re.findall(oldwords_pat, url)[0]
                newwords_pat = '[\s\S]*\n(.*)'
                newwords = re.findall(newwords_pat, all_content)[0]
                new_url = url.replace(old_words, newwords)
                if(debug):
                    print("real url is " + new_url)
                sub_all_content = requests.get(new_url).text
                # all_content = request.urlopen(new_url).read().decode('utf-8') # 获取M3U8的文件内容
                file_line = sub_all_content.splitlines()  # 读取文件里的每一行
            elif ((url.find('cdn.letv-cdn.com') != -1) or (url.find('eth.ppzuida.com') != -1)):
                # 换一种拼接方式
                if(debug):
                    print('from cdn.letv-cdn.com || eth.ppzuida.com')
                oldwords_pat = 'http[s]?://.*?/(.*)'
                old_words = re.findall(oldwords_pat, url)[0]
                if(debug):
                    print(old_words)
                newwords_pat = '.*?/(.*.m3u8).*'                    
                newwords = re.findall(newwords_pat, all_content)[0]
                if(debug):
                    print(all_content)
                    print("newwords " + newwords)
                new_url = url.replace(old_words, newwords)
                if(debug):
                    print(new_url)
                all_content = requests.get(new_url).text
                # all_content = request.urlopen(new_url).read().decode('utf-8') # 获取M3U8的文件内容
                file_line = all_content.splitlines()  # 读取文件里的每一行
            else:
                '''
                TODO 其他仓库地址更换最后的index.m38u,
                兼容:
                1. 下载url：https://video.letv-cdn.com/20180223/63M9f5sY/index.m3u8
                内容如下：
                #EXTM3U
                #EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1000000,RESOLUTION=1280x528
                1000kb/hls/index.m3u8
                解析成这样：https://video.letv-cdn.com/20180223/63M9f5sY/1000kb/hls/index.m3u8

                2. download url is http://cn2.okokyun.com/20180128/4dozvYwY/index.m3u8
                real url is http://cn2.okokyun.com/20180128/4dozvYwY/800kb/hls/index.m3u8
                '''
                if(debug):
                    print('from other url,if fail contact me:')
                oldwords_pat = '.*/(.*)'
                old_words = re.findall(oldwords_pat, url)[0]
                newwords_pat = '[\s\S]*\n(.*)'
                newwords = re.findall(newwords_pat, all_content)[0]
                new_url = url.replace(old_words, newwords)
                if(debug):
                    print("real url is " + new_url)
                sub_all_content = requests.get(new_url).text
                # all_content = request.urlopen(new_url).read().decode('utf-8') # 获取M3U8的文件内容
                file_line = sub_all_content.splitlines()  # 读取文件里的每一行

        # 通过判断文件头来确定是否是M3U8文件
        if file_line[0] != "#EXTM3U":
            raise BaseException(u"非M3U8的链接")
        else:
            # 判断有无子m3u8文件
            unknow = True  # 用来判断是否找到了下载的地址
            if(debug):
                print(new_url)
            ''' 
                #EXTM3U
                #EXT-X-VERSION:3
                #EXT-X-TARGETDURATION:15
                #EXT-X-MEDIA-SEQUENCE:0
                #EXTINF:6.625,
                /20180430/smshC8Vz/1000kb/hls/a1APgIK2671000.ts
                #EXTINF:10.417,
                /20180430/smshC8Vz/1000kb/hls/a1APgIK2671001.ts
                #EXTINF:3.083,
                /20180430/smshC8Vz/1000kb/hls/a1APgIK2671002.ts
                #EXTINF:10.375,
                /20180430/smshC8Vz/1000kb/hls/a1APgIK2671003.ts
                #EXTINF:10.167,
                /20180430/smshC8Vz/1000kb/hls/a1APgIK2671004.ts
                #EXTINF:10.375,
                /20180430/smshC8Vz/1000kb/hls/a1APgIK2671005.ts
                #EXTINF:3.042,
                /20180430/smshC8Vz/1000kb/hls/a1APgIK2671006.ts
                ...
                #EXT-X-ENDLIST
            '''
            for index, line in enumerate(file_line):
                if "EXTINF" in line:  #根据规律得知，每一行都是取下一行的内容  
                    unknow = False
                    # 拼出ts片段的URL
                    c_fule_name = str(file_line[index + 1]) # index + 1是取下一行
                    c_fule_name_new = c_fule_name
                    if new_url.find('cdn.letv-cdn.com') != -1 or new_url.find('eth.ppzuida.com') != -1:
                        oldwords_pat = 'http[s]?://.*?/(.*)'
                        fule_pat = '.*/(.*)'
                        c_fule_name_new = re.findall(fule_pat, c_fule_name)[0]
                    else:
                        oldwords_pat = '.*/(.*)'
                    old_words = re.findall(oldwords_pat, new_url)[0]
                    download_url = new_url.replace(old_words, c_fule_name)
                    local_name = download_path + "/" + c_fule_name_new
                    if False:   #调试用
                        print(download_url)
                        return
                    request.urlretrieve(url=download_url,filename=local_name)
            if unknow:
                raise BaseException("未找到对应的下载链接")
            else:
                print(u"下载完成")

    def simpledownload(self, m3u8content, download_path):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # Accept-Encoding: gzip, deflate #最好不要写或者写成Accept-Encoding: utf-8,gb2312
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36",
            "Connection": "keep-alive",     #或者"Proxy-Connection": "keep-alive"
            "referer":"qq.com"  #一般为它的首页
        }
        cjar = cookiejar.CookieJar()
        opener = request.build_opener(request.HTTPCookieProcessor(cjar))
        headall = []
        for key,value in headers.items():
            item = (key,value)
            headall.append(item)
        opener.addheaders = headall
        request.install_opener(opener)
        file_line = m3u8content.splitlines()  # 读取文件里的每一行
        for index, line in enumerate(file_line):
            if "EXTINF" in line:  #根据规律得知，每一行都是取下一行的内容  
                # 拼出ts片段的URL
                c_fule_name = str(file_line[index + 1]) # index + 1是取下一行
                c_fule_name_new = c_fule_name
                fule_pat = '.*'
                c_fule_name_new = re.findall(fule_pat, c_fule_name)[0]
                download_url = 'https://w.bwzybf.com/2018/06/15/5oMLtdRKnCOPNTJK/' + c_fule_name_new
                # download_url = 'http://eth.ppzuida.com/20171122/OuFFyQ3R/800kb/hls/' + c_fule_name_new
                local_name = download_path + "/" + c_fule_name_new
                # requests.get(download_url)
                request.urlretrieve(url=download_url, filename=local_name)

class MergeFile():
    '''
    合并ts的格式:
    ./ffmpeg -i concat:"out002.ts|out003.ts|out004.ts" -acodec copy -vcodec copy -f mp4 cat.mp4
    或者
    ffmpeg -i "concat:D:/downloadmerge2/026d4c8b18b000.ts|...|D:/downloadmerge2/026d4c8b18b017.ts|D:/downloadmerge2/026d4c8b18b018.ts|D:/downloadmerge2/026d4c8b18b019.ts|D:/downloadmerge2/026d4c8b18b02
    :/downloadmerge2/026d4c8b18b021.ts" -bsf:a aac_adtstoasc -c copy -vcodec copy 1.mp4
    '''

    '''
    合并mp4的格式:
    ffmpeg -y -f concat -i mp4list.txt -c copy bingxue.mp4
    '''

    def __init__(self):
        pass

    def merge_ts(self, source_dir, output_dir, des_filename):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) # python创建多层目录的方式
        tempname = 1
        content = ""

        lists = [(i, os.stat(source_dir + i).st_mtime) for i in os.listdir(source_dir)]
        '''
        lists格式
        [
            ('026d4c8b18b000.ts', 1528077232.3878698),
            ('026d4c8b18b001.ts', 1528077233.467319),
            ...
        ]
        '''
        lists = sorted(lists, key=lambda x: x[1])   # x[0] = '026d4c8b18b000.ts' x[1] = 1528077232.3878698
        groups = [lists[i : (i + 50)] for i in range(0, len(lists), 50)]
        
        for lis in groups:
            cmd = "cd %s && ffmpeg -i \"concat:" %output_dir
            for file in lis:
                if file != '.DS_Store':
                    file_path = os.path.join(source_dir, file[0])
                    cmd += file_path + '|'
            cmd = cmd[:-1]  # 去掉最后的符号|
            # cmd += '" -bsf:a aac_adtstoasc -c copy -vcodec copy %s.mp4' %tempname
            cmd += '" -y -ac 2 -acodec copy -vcodec copy -f mp4 %s.mp4' %tempname
            # ffmpeg -i concat:"out002.ts|out003.ts|out004.ts" -acodec copy -vcodec copy -f mp4 cat.mp4
            try:
                os.system(cmd)
                content += "file '%s.mp4'\n" %tempname
                tempname = tempname + 1
            except:
                print("Unexpected error")

        fp = open("%smp4list.txt" %output_dir,'a+')
        fp.write(content)
        fp.close()

        # 合并mp4文件
        mp4cmd = "cd %s && ffmpeg -y -f concat -i mp4list.txt -c copy %s"%(output_dir,des_filename)
        if(debug):
            print('合并mp4文件命令：' + mp4cmd)
        os.system(mp4cmd)
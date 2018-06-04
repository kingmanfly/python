import os
import json

from cracklib import ParseVideoUrl
from cracklib import DownloadResourse
from cracklib import MergeFile

urldict = { 
    'bingxue':
        {   
            'url' : 'http://www.iqiyi.com/v_19rrlhpgbg.html',   # 冰雪奇缘
            'name' : 'bingxue'     # 红海行动
        },
    'honghai':
        {   
            'url' : 'http://www.iqiyi.com/v_19rr7plwdc.html',   # 红海行动
            'name' : 'honghai'     # 红海行动
        }
    }

parse_vidio = ParseVideoUrl(urldict['bingxue']['url'])

# 步骤一、准备线路
parse_vidio.prepare_line()

# 步骤二、载入需要请求的url
real_url_page_data = parse_vidio.load_real_url()
jsondata = json.loads(real_url_page_data)

# 步骤三、优化线路
parse_vidio.prepare_load_goal_url(jsondata)

# 步骤四、获取要下载的url真实地址
download_url = parse_vidio.load_goal_url(jsondata)

# 步骤五、开始下载
name = urldict['bingxue']['name']
downloaddir = 'D:/crackvideo/download/' + name + '/'

downloadresource = DownloadResourse()
downloadresource.download(download_url, downloaddir)

# 步骤六、合并下载好的ts文件
merge_file = MergeFile()
outputdirs = "D:/crackvideo/outputdir/" + name + '/'
filename = name + ".mp4"

merge_file.merge_ts(downloaddir, outputdirs, filename)

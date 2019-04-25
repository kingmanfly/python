import json

from cracklib import ParseVideoUrl
from cracklib import DownloadResourse
from cracklib import MergeFile

urldict = {
    'nima':
        {   
            'url' : 'http://www.iqiyi.com/v_19rr7pkf30.html',
            'name' : 'nima'     # 我是你妈
        },
    'jizhang':
        {   
            'url' : 'http://www.iqiyi.com/v_19rrfowvh8.html',
            'name' : 'jizhang'     # 萨利机长
        },
    'qingdi':
        {   
            'url' : 'http://www.iqiyi.com/v_19rrk3nops.html',
            'name' : 'qingdi'     # 全民情敌
        },
    'kekexili':
        {   
            'url' : 'http://www.iqiyi.com/v_19rrh1gubo.html',
            'name' : 'kekexili'     # 可可西里的美丽传说
        },
    '21kela':
        {   
            'url' : 'http://www.iqiyi.com/v_19rrel12t4.html',
            'name' : '21kela'     # 21克拉
        },
    'bingxue':
        {   
            'url' : 'http://www.iqiyi.com/v_19rrlhpgbg.html',   # 冰雪奇缘
            'name' : 'bingxue'     # 红海行动
        },
    'xinxiju':
        {   
            'url' : 'https://www.iqiyi.com/v_19rqrgpp5k.html',   # 新喜剧之王
            'name' : 'xinxiju'     # 新喜剧之王
        },
    'honghai':
        {   
            'url' : 'http://www.iqiyi.com/v_19rr7plwdc.html',   # 红海行动
            'name' : 'honghai'     # 红海行动
        }
    }

parse_vidio = ParseVideoUrl(urldict['honghai']['url'])

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
name = urldict['nima']['name']
downloaddir = 'D:/crackvideo/download/' + name + '/'

downloadresource = DownloadResourse()
downloadresource.download(download_url, downloaddir)

# 步骤六、合并下载好的ts文件
merge_file = MergeFile()
outputdirs = "D:/crackvideo/outputdir/" + name + '/'
filename = name + ".mp4"

merge_file.merge_ts(downloaddir, outputdirs, filename)

import json

from cracklib import DownloadResourse
from cracklib import MergeFile

name = 'nima'
downloaddir = 'D:/crackvideo/download/' + name + '/'

downloadresource = DownloadResourse()

f = open('D:/crackvideo/download/aa.txt','r') # 读模式
content = f.read()
downloadresource.simpledownload(content, downloaddir)

merge_file = MergeFile()
outputdirs = "D:/crackvideo/outputdir/" + name + '/'
filename = name + ".mp4"

merge_file.merge_ts(downloaddir, outputdirs, filename)
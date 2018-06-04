from cracklib import MergeFile

# 步骤六、合并下载好的ts文件
name = 'whitesnow'
merge_file = MergeFile()
downloaddir = 'D:/crackvideo/download/' + name + '/'
outputdirs = "D:/crackvideo/outputdir/" + name + '/'
filename = name + ".mp4"

merge_file.merge_ts(downloaddir, outputdirs, filename)
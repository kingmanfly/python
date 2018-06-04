import os

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
dirs = "D:/Projects/github/python/research/download"
outputdirs = "D:/outputdir/"
filename = "bingxue.mp4"
tempname = 1
content = ""

lists = os.listdir(dirs)
groups = [lists[i : (i + 100)] for i in range(0, len(lists), 100)]

for lis in groups:
    cmd = "cd %s && ffmpeg -i \"concat:" %outputdirs
    for file in lis:
        if file != '.DS_Store':
            file_path = os.path.join(dirs, file)
            cmd += file_path + '|';
    cmd = cmd[:-1]  # 去掉最后的符号|
    # cmd += '" -bsf:a aac_adtstoasc -c copy -vcodec copy %s.mp4' %tempname
    cmd += '" -acodec copy -vcodec copy -f mp4 %s.mp4' %tempname
    # ffmpeg -i concat:"out002.ts|out003.ts|out004.ts" -acodec copy -vcodec copy -f mp4 cat.mp4
    try:
        os.system(cmd)
        content += "file '%s.mp4'\n" %tempname
        print("~~~~~~~~~~~~~~···content%s" %content)
        tempname = tempname + 1
    except:
        print("Unexpected error")

fp = open("%smp4list.txt"%outputdirs,'a+')
fp.write(content)
fp.close()

# 合并mp4文件
mp4cmd = "cd %s && ffmpeg -y -f concat -i mp4list.txt -c copy %s"%(outputdirs,filename)
print('合并mp4文件命令：' + mp4cmd)
os.system(mp4cmd)
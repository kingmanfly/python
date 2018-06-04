import re
import requests
import os

""" url = 'http://youku.cdn-tudou.com/20180509/5830_9bd173fc/index.m3u8'
all_content = requests.get(url).text  # 获取M3U8的文件内容
print(all_content)
oldwords_pat = '.*/(.*)'
old_words = re.findall(oldwords_pat, url)[0]
print(old_words)

newwords_pat = '\s\S*\n(.*)'
newwords = re.findall(newwords_pat, all_content)[0]
print(newwords)

print(url.replace(old_words, newwords))
 """
# jj = '{"Moren":"http://y2.xsdd.org:91/ifr?url=2DiVMBUA2GrJEMaGuXv3l4TOrnts%2bYS7laQHqQMROnbI5dDlHPJsJSUiRDsqRfHMIt3ME40kpHTagcd1CpaMiQ%3d%3d\u0026type=m3u8"'
# url_pat = '(http[s]?://.*?)\?'

# print(re.findall(url_pat, jj))

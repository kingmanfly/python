import re
from urllib import request
from urllib import error

def craw(url, page):
    goal_content_pattern = '<div id="plist".+? <div class="page clearfix">'
    pic_pattern = '<img width="220" height="220" data-img="1" src="//(.+?\.jpg)">'
    html1 = request.urlopen(url).read()
    html1 = str(html1)
    result1 = re.findall(goal_content_pattern, html1)
    result1 = result1[0]
    
    imagelist = re.findall(pic_pattern, result1)
    x = 1
    for imageurl in imagelist:
        imagename = "D:/training/python/resource/" + str(page) + "_" + str(x) + ".jpg"
        imageurl = "http://" + imageurl
        try:
            request.urlretrieve(imageurl, filename=imagename)
        except error.URLError as e:
            if hasattr(e, "code"):
                x+=1
            if hasattr(e, "reason"):
                x+=1
        x+=1

for i in range(1,3):
    url = "http://list.jd.com/list.html?cat=9987,653,655&page=" + str(i)
    craw(url, i)
            


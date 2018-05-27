from urllib import request
import re

def getcontent(url, page):
    # 模拟浏览器
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
    opener = request.build_opener()
    opener.addheaders = [headers]
    request.install_opener(opener)
    
    data = request.urlopen(url).read().decode('utf-8')
    
    # 使用左边的面板内容
    root_pattern = '<div id="content-left" class="col1">([\s\S]*?)<div class="col2">'
    root_content = re.findall(root_pattern, data)

    # 构建段子内容提取的正则表达式
    content_pattern = '<div class="content">\s*<span>([\s\S]*?)</span>[\s\S]*?</div>'
    contentlist = re.findall(content_pattern, root_content[0])
    x = 1
    for content in contentlist:
        
        # 先把空格、回车符去掉
        content = content.strip()

        # 用字符串作为变量名，先将对应字符串赋给一个变量
        name = "content" + str(x)

        # 通过exec函数实现用字符串作为变量名并赋值
        exec(name + '=content')
        x += 1

    # 构建对应用户提取的正则表达式
    user_pattern = '<div class="author clearfix">([\s\S]*?)<h2>([\s\S]*?)</h2>([\s\S]*?)web-list-content'
    userlist = re.findall(user_pattern, root_content[0])
    y = 1
    for user in userlist:
        name = "content" + str(y)
        print("用户" + str(page) + str(y) + "是：" + user[1].strip())
        print("")
        exec("print("+name+")")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        y += 1

for i in range(1,3):
    url = "https://www.qiushibaike.com/8hr/page/" + str(i)
    getcontent(url, i)
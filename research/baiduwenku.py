from selenium import webdriver
from bs4 import BeautifulSoup
import time

# ***selenium 自动操作网页***
options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"')   #设置设备代理
driver = webdriver.Chrome(chrome_options=options)

driver.get('https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html') 

# 拖动网页到可见的元素去
page = driver.find_element_by_xpath("//div[@id='html-reader-go-more']")
driver.execute_script('arguments[0].scrollIntoView();', page)

# 点击按钮
nextpage = driver.find_element_by_xpath("//span[@class='moreBtn goBtn']")
nextpage.click()                                           

# ***对打开的html进行分析***
html = driver.page_source

bf1 = BeautifulSoup(html, 'lxml')
# bf1 = BeautifulSoup(html, 'html.parser')

# 获得文章标题
title = bf1.find_all('h1', class_='reader_ab_test with-top-banner')
bf2 = BeautifulSoup(str(title), 'lxml')
title = bf2.find('span')
title = title.get_text()
filename = title + '.txt'
print(title)

# 获得文章内容
texts_list = []
result = bf1.find_all('div', class_='ie-fix')
for each_result in result:
    bf3 = BeautifulSoup(str(each_result), 'lxml')
    texts = bf3.find_all('p')
    for each_text in texts:
        texts_list.append(each_text.string)
contents = ''.join(texts_list).replace('\xa0', '')

fhandle = open('D:/training/python/2.txt', 'wb')
fhandle.write(contents.encode('utf-8'))
fhandle.close()

driver.close()
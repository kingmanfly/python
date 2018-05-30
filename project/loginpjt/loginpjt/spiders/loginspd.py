# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from scrapy.http import Request, FormRequest

class LoginspdSpider(scrapy.Spider):
    name = 'loginspd'
    allowed_domains = ['douban.com']

    header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}

    def start_requests(self):
        return [Request("https://accounts.douban.com/login", 
        headers = self.header, 
        meta={"cookiejar":1},
        callback=self.parse)]

    def parse(self, response):
        print("parse~~~~~~~~~~")
        print(response)
        # 获取验证码图片所在的地址，获取后给captcha变量，此时captcha为一个列表
        captcha = response.xpath('//img[@id="captcha_image"]/@src').extract()
        if len(captcha) > 0:
            print('有验证码')
            localpath = "D:/training/python/source/captcha.png"
            request.urlretrieve(captcha[0], filename=localpath)
            print("请查看本地的captha.png文件，并输入对应的验证码")
            captcha_value = input()
            # 设置要传递的post数据
            data = {
                "form_email":"lijinwei_123@126.com",
                "form_password":"kingman123",
                "captcha-solution": captcha_value,
                "redir":"https://www.douban.com/people/179184407/"
            }
        else:
            print('没有验证码')
            data = {
                "form_email":"lijinwei_123@126.com",
                "form_password":"kingman123",
                "redir":"https://www.douban.com/people/179184407/"
            }
        print("登录中")
        # 通过FormRequest.from_response()进行登录
        return [FormRequest.from_response(response,
            headers = self.header,
            meta = {"cookiejar":1},
            formdata = data,
            callback = self.next)]
    
    def next(self, response):
        print("此时已经完成登录并爬取到了个人中心的页面的数据了")
        xtitle = "/html/head/title/text()"
        xnotetitle = "//div[@class='note-header pl2']/a/@title"
        xnotetime = "//div[@class='note-header pl2']//span[@class='pl']/text()"
        xnotecontent = "//div[@class='mbtr2']//div[@class='note']/text()"
        xnoteurl = "//div[@class='note-header pl2']/a/@href"

        title = response.xpath(xtitle).extract()
        notetitle = response.xpath(xnotetitle).extract()
        notetime = response.xpath(xnotetime).extract()
        notecontent = response.xpath(xnotecontent).extract()
        noteurl = response.xpath(xnoteurl).extract()

        print("网页标题为" + title[0])
        
        for i in range(0, len(notetitle)):
            print("第"+str(i+1)+ "篇文章信息如下：")
            print("文章标题为 " + notetitle[i])
            print("文章发表时间为 " + notetime[i])
            print("文章内容为 " + notecontent[i])
            print("文章链接为 " + noteurl[i])


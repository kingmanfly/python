# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import request

from hexunpjt.items import HexunpjtItem
from scrapy.http import Request

class MyhexunspdSpider(scrapy.Spider):
    name = 'myhexunspd'
    allowed_domains = ['hexun.com']
    uid = '14168699'
    def start_requests(self):
        # 首次爬取模拟成浏览器进行
        url = "http://"+ str(self.uid) +".blog.hexun.com/p1/default.html"
        header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
        print(url)
        print(header)
        yield Request(url, headers = header)

    def parse(self, response):
        item = HexunpjtItem()
        item['name'] = response.xpath('//span[@class="ArticleTitleText"]/a/text()').extract()
        item['url'] = response.xpath('//span[@class="ArticleTitleText"]/a/@href').extract()
        # 接下来使用urllib和re模块获取评论数和阅读数
        # 首先提取春初评论数和点击数的正则表达式
        print('~~~~~~~~~~~~~~~~~')
        print(item['name'])
        print(item['url'])
        
        pat_click = '<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'
        hintcurl = re.findall(pat_click, str(response.body))[0]

        headers2 = ("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
        opener = request.build_opener()
        opener.addheaders = [headers2]
        request.install_opener(opener)
        data = request.urlopen(hintcurl).read()

        pat_hits = "click\d*?','(\d*?)'"

        pat_comnum = "comment\d*?','(\d*?)'"

        item['hits'] = re.findall(pat_hits, str(data))
        item['comment'] = re.findall(pat_comnum, str(data))

        yield item

        pat_page_number = "blog.hexun.com/p(.*?)/"
        data2 = re.findall(pat_page_number, str(response.body))

        if len(data2) >=2:
            totalurl = data2[-2]
        else:
            totalurl = 1
        print(str(totalurl))

        for i in range(2, int(totalurl) + 1):
            nexturl = "http://"+ str(self.uid) + ".blog.hexun.com/p" + str(i) + "/default.html"
            yield Request(nexturl, callback=self.parse, headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"})


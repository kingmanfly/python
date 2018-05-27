# -*- coding: utf-8 -*-
import scrapy
import re
from qtpjt.items import QtpjtItem
from scrapy.http import Request

class QtspdSpider(scrapy.Spider):
    name = 'qtspd'
    allowed_domains = ['58pic.com']
    start_urls = ['http://www.58pic.com/tupian/yuebing-0-0-1.html']

    def parse(self, response):
        item = QtpjtItem()
        pat_url = "(http://pic.qiantucdn.com/58pic/.*?).jpg"
        item['picurl'] = re.findall(pat_url, str(response.body), re.I)

        pat_local = "http://pic.qiantucdn.com/58pic/.*?/.*?/.*?/(.*?).jpg"

        item['picid'] = re.findall(pat_local, str(response.body), re.I)
        yield item

        # 通过for循环遍历1~3页的内容
        for i in range(2, 4):
            nexturl = "http://www.58pic.com/tupian/yuebing-0-0-" + str(i)+ ".html"
            yield Request(nexturl, callback=self.parse)
            
 
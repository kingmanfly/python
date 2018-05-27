# -*- coding: utf-8 -*-
import scrapy


class FilenameSpider(scrapy.Spider):
    name = 'filename'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass

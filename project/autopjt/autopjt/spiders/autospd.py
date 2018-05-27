# -*- coding: utf-8 -*-
import scrapy
from autopjt.items import AutopjtItem
from scrapy.http import Request


class AtospdSpider(scrapy.Spider):
    name = 'autospd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/pg1-cid4003599.html']

    def parse(self, response):
        item = AutopjtItem()
        # 通过个XPath表达式分别提取商品的名称、价格、链接、评论数等信息
        item['name'] = response.xpath('//a[@class="pic"]/@title').extract()
        item['price'] = response.xpath('//span[@class="price_n"]/text()').extract()
        item['link'] = response.xpath('//a[@class="pic"]/@href').extract()
        item['comnum'] = response.xpath('//a[@name="itemlist-review"]/text()').extract()
        # 提取完返回item
        yield item

        # 接下来很关键，通过循环自动爬取1~3页
        for i in range(1, 3):
            url = "http://category.dangdang.com/pg" + str(i) + "-cid4003599.html"
            # 通过yield返回Request，并指定要爬取的网址的回调函数
            # 实现自动爬取
            yield Request(url, callback=self.parse)


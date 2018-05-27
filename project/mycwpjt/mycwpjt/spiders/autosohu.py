# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mycwpjt.items import MycwpjtItem

class AutosohuSpider(CrawlSpider):
    name = 'autosohu'
    allowed_domains = ['sohu.com']
    start_urls = ['http://news.sohu.com/']

    rules = (
        Rule(LinkExtractor(allow=('.*?/n.*?shtml'), allow_domains=('sohu.com')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = MycwpjtItem()
        # 获取新闻标题
        i['name'] = response.xpath("/html/head/title/text()").extract()

        # 获取当前新闻的网页链接
        i['link'] = response.xpath("//link[@rel='canonical']/@href").extract()
        
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

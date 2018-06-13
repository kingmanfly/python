# -*- coding: utf-8 -*-
import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from pornhub.pornhub_type import PH_TYPES
from pornhub.items import PornhubItem
import re
import json

class Spider(CrawlSpider):
    name = 'pornHubSpider'
    host = 'https://www.pornhub.com'
    allowed_domains = ['pornhub.com']
    start_urls = list(set(PH_TYPES))

    test = True
    def start_requests(self):
        print('start_requests')
        print(self.test)
        for ph_type in self.start_urls:
            yield Request(url='https://www.pornhub.com/%s' % ph_type,
                          callback=self.parse_ph_key)

    def parse_ph_key(self, response):
        divs = response.xpath('//div[@class="phimage"]')
        for div in divs:
            viewkey = re.findall('viewkey=(.*?)"', div.extract())
            yield Request(url='https://www.pornhub.com/embed/%s' % viewkey[0],
                          callback=self.parse_ph_info)
        url_next = response.xpath(
            '//a[@class="orangeButton" and text()="Next "]/@href').extract()
        if url_next:
            if self.test:
                yield Request(url=self.host + url_next[0],
                          callback=self.parse_ph_key)
                self.test = False

    def parse_ph_info(self, response):
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        phItem = PornhubItem()
        _ph_info = re.findall('var flashvars =(.*?),\n', response.body)

        _ph_info_json = json.loads(_ph_info[0])
        duration = _ph_info_json.get('video_duration')
        phItem['video_duration'] = duration
        title = _ph_info_json.get('video_title')
        phItem['video_title'] = title
        image_url = _ph_info_json.get('image_url')
        phItem['image_url'] = image_url
        link_url = _ph_info_json.get('link_url')
        phItem['link_url'] = link_url
        quality_480p = _ph_info_json.get('quality_480p')
        phItem['quality_480p'] = quality_480p
        yield phItem

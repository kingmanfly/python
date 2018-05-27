# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AutopjtItem(scrapy.Item):
    # define the fields for your item here like:

    # 商品名
    name = scrapy.Field()

    # 商品价格
    price = scrapy.Field()

    # 商品链接
    link = scrapy.Field()

    # 商品评论数
    comnum = scrapy.Field()

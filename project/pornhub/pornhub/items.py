# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class PornhubItem(Item):
    # define the fields for your item here like:
    # 视频的标题,并作为唯一标识.
    video_title = Field()

    # 视频的封面链接
    image_url = Field()

    # 视频的时长，以 s 为单位
    video_duration = Field()

    # 视频480p的 mp4 下载地址
    quality_480p = Field()

    video_views = Field()
    video_rating = Field()

    # 视频调转到PornHub的链接
    link_url = Field()

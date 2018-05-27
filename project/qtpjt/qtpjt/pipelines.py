# -*- coding: utf-8 -*-
from urllib import request

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QtpjtPipeline(object):
    def process_item(self, item, spider):
        # 一页中有多张图片，通过for循环依次储存图片
        for i in range(0, len(item['picurl'])):
            thispic = item['picurl'][i]
            trueurl = thispic + ".jpg"
            localpath = "D:/training/python/source/project/qtpjt/download/" + item['picid'][i] + ".jpg"
            request.urlretrieve(trueurl, filename=localpath)
        return item

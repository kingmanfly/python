# -*- coding: utf-8 -*-
import codecs
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutopjtPipeline(object):
    def __init__(self):
        self.file = codecs.open("D:/training/python/source/project/autopjt/autopjt/data/mydata2.json", "wb",encoding='utf-8')

    def process_item(self, item, spider):
        # item是一页的信息
        # 每一页中包含多个商品信息，所以可以通过循环，每次处理一个商品
        # 其中len(itme['name'])为当前页商品的总数，一次遍历
        for j in range(0, len(item['name'])):
            name = item['name'][j]
            price = item['price'][j]
            link = item['link'][j]
            comnum = item['comnum'][j]
            # 重新组合成字典
            goods = {"name":name, "price":price, "link":link, "comnum":comnum}
            i = json.dumps(dict(goods), ensure_ascii = False)
            # 每条数据后加上换行
            line = i + "\n"
            # 将数据写入mydata.json
            self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

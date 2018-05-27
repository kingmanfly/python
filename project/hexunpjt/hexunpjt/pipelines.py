# -*- coding: utf-8 -*-
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HexunpjtPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",user="root",passwd="root",db="hexun")
    
    def process_item(self, item, spider):
        # 每一个博文列表页包含多条博文信息，通过for循环来处理各个博文
        for j in range(0, len(item['name'])):
            name = item['name'][j]
            url = item['url'][j]
            hits = item['hits'][j]
            comment = item['comment'][j]
            print(name)
            # 构造对应的sql语句，将获取到的数据插入数据库
            sql = "insert into myhexun(name, url,hits, comment) values('"+name+"','"+url+"','"+hits+"', '"+comment+"')"
            self.conn.query(sql)
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
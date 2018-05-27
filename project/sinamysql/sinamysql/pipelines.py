# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinamysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",user="root",passwd="root",db="mypydb")
    
    def process_item(self, item, spider):
        name = item['name'][0]
        key = item['keywd'][0]
        sql="insert into mytb(title,keywd) VALUES('" + name + "+ ','" + key + "')"
        self.conn.query(sql)
        self.conn.commit()
        print(name)
        return item

    def close_spider(self, spider):
        self.conn.close()

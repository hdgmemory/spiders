# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
class TaobaoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('127.0.0.1')
        self.db=self.client['Taobao']
    def process_item(self, item, spider):
        self.db['baijiu'].insert(dict(item))
        return item


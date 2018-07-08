# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import pymongo

from scrapy.conf import settings

class MzituPipeline(object):
    def __init__(self):
        conn = pymongo.MongoClient(host='localhost', port=27017)
        db = conn['mzitu']
        self.collection = db['img_info']

    def process_item(self, item, spider):
        self.collection.update({'img_box_url': item['img_box_url']}, {'$set': item}, True)
        return item


class MzituRedisPipeline(object):
    def __init__(self):
        self.redis = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'])

    def process_item(self, item, spider):
        self.redis.lpush('mzitu:start_urls', item['img_box_url'])
        return item
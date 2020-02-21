# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from otomoto import settings
import logging


class OtomotoPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if self.collection.find({'Id': item['Id']}).count() == 1:
            logging.info('Car already exist in database !')
        else:
            self.collection.insert(dict(item))
            logging.info("Car added to MongoDB")
            return item

    def __del__(self):
        self.connection.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook
import pymongo
import pymysql
import logging

logger = logging.getLogger(__name__)

class LogPipeline(object):
    def process_item(self, item, spider):
        logging.warning("*-*pipeline的warning信息*-*")
        return item


class TaobaoPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['商品名称', '价格', '店铺地址', '销售量', '商品链接', '图片链接'])

    def process_item(self, item, spider):
        line = [item['raw_title'], item['view_price'], item['item_loc'], item['view_sales'], item['shop_link'],
                item['pic_url']]
        self.ws.append(line)
        keys = spider.settings.get('KEYS')
        self.wb.save(keys + '.xlsx')
        print('已保存到', keys, '.xlsx')
        return item

'''
import csv


class TaobaoPipeline(object):
    def open_spider(self, spider):
        self.file = open('D://taobao/淘宝信息.csv', 'w')

    def process_item(self, item, spider):
        # 将信息写进csv文件中
        file_names = ['item_loc', 'pic_url', 'raw_title', 'view_price', 'view_sales', 'shop_link']
        for name in file_names:
            if item[name] == None:
                item[name] = 'there is no item data'
        dict_writer = csv.DictWriter(self.file, fieldnames=file_names)
        dict_writer.writerow(dict(item))
        return item

    def close_item(self, spider):
        self.file.close()

'''
class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.collection
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()



class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        #print(item['raw_title'])
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item
        


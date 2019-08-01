# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    collection = table = '华为Nova2s'
    item_loc = scrapy.Field()
    pic_url = scrapy.Field()
    raw_title = scrapy.Field()
    view_price = scrapy.Field()
    view_sales = scrapy.Field()
    shop_link = scrapy.Field()
    pass

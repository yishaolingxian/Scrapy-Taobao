# -*- coding: utf-8 -*-
import json
import random
import re
import time
from urllib import parse
import scrapy
from scrapy.http import Request
from Taobao.items import TaobaoItem
from Taobao.tools import getcookiefromchrome



class TaobaospiderSpider(scrapy.Spider):
    name = 'taobao'
    # allowed_domains = ['taobao.com']
    cookie = getcookiefromchrome()

    def get_time_stamp(self):
        time_stamp = int(round(time.time() * 1000))
        ran_num = random.randint(100, 3000)
        ksts = str(time_stamp) + '_' + str(ran_num)
        return ksts, str(ran_num)

    # 这里我直接声明了一个方法，用于获取时间戳和callback，返回两者的元组。

    def start_requests(self):
        # 这里我们去掉了start_urls，直接用这个方法来构造初始请求
        data_fir = {
            'q': self.settings.get('KEYS'),
            'imgfile': '',
            'commend': 'all',
            'ssid': 's5-e',
            'search_type': 'item',
            'sourceId': 'tb.index',
            'spm': 'a21bo.2017.201856-taobao-item.1',
            'ie': 'utf8',
            'initiative_id': 'tbindexz_20170306'

        }
        url = 'https://s.taobao.com/search?' + parse.urlencode(data_fir)
        # 构造参数的链接的方式
        yield Request(url=url, cookies=self.cookie, callback=self.parse)


    def parse(self, response):
        #time.sleep(1)
        pattern = re.compile('g_page_config = ({.*?});', re.S)
        # 匹配出json型的数据，用正则。
        json_data = re.search(pattern, response.text).group(1)
        json_l = json.loads(json_data)
        item = TaobaoItem()
        for datas in json_l.get('mods').get('itemlist').get('data').get('auctions'):
            item['item_loc'] = datas.get('item_loc')
            item['pic_url'] = 'https:' + datas.get('pic_url')
            item['raw_title'] = datas.get('raw_title')
            item['shop_link'] = 'https:' +datas.get('shopLink')
            item['view_price'] = datas.get('view_price')
            item['view_sales'] = datas.get('view_sales')
            shop_link =  datas.get('shopLink')
            #pages = datas.get('totalPage')
            file_names = ['item_loc', 'pic_url', 'raw_title', 'view_price', 'view_sales', 'shop_link']
            for name in file_names:
                if item[name] == None:
                    item[name] = 'there is no item data'
            yield item
        #print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   '+'https:',shop_link)
        next_partial_url = json_l.get('mainInfo').get('modLinks').get('pager')
        # print('next_partial_url:','https:'+next_partial_url)
        times = self.get_time_stamp()
        data_value = 44
        other_data = {
            'data-key': 's',
            'data-value': str(data_value),
            '_ksTS': times[0],
        }
        # print('other_date:',parse.urlencode(other_data))
        next_url = 'https:' + next_partial_url + '&' + parse.urlencode(other_data)
        # print('-------------------',next_url)
        # 这里获得第二页的基本链接，要加上时间戳
        data_values = data_value + 44
        yield Request(url=next_url, meta={'data_value': data_values}, cookies=self.cookie, callback=self.parse_item)
        # meta参数用于传递页数

    def parse_item(self, response):
        #time.sleep(1)
        pattern = re.compile('g_page_config = ({.*?});', re.S)
        # 匹配出json型的数据，用正则。
        json_data = re.search(pattern, response.text).group(1)
        json_l = json.loads(json_data)
        page = re.findall(r'\"totalPage\"\:\d+',response.text)
        totalPage = eval(page[0].split(':')[1])
        #print('+++++++++++++++++++++++++++++++++++++',totalPage)
        #print(json_l)
        for datas in json_l.get('mods').get('itemlist').get('data').get('auctions'):
            item = TaobaoItem()
            item['item_loc'] = datas.get('item_loc')
            item['pic_url'] = 'https:' + datas.get('pic_url')
            item['raw_title'] = datas.get('raw_title')
            item['shop_link'] = datas.get('shop_Link')
            item['view_price'] = datas.get('view_price')
            item['view_sales'] = datas.get('view_sales')
            
            file_names = ['item_loc', 'pic_url', 'raw_title', 'view_price', 'view_sales', 'shop_link']
            for name in file_names:
                if item[name] == None:
                    item[name] = 'there is no item data'
            yield item
        for i in range(totalPage-2):
            pager = json_l.get('mainInfo').get('modLinks').get('pager')
            print('爬取一页结束')
            # 调试信息
            # 这里获得了下一页的基本链接，还有加上时间戳
            times = self.get_time_stamp()
    
            other_data = {
                'data-key': 's',
                'data-value': str(response.meta['data_value']),
                '_ksTS': times[0]
            }
            next_url = 'https:' + pager + '&' + parse.urlencode(other_data)
            #print('******************',next_url)
            # 这里获得第二页的基本链接，要加上时间戳
            data_values = response.meta['data_value'] + 44
            yield Request(url=next_url, meta={'data_value': data_values}, cookies=self.cookie, callback=self.parse_item)


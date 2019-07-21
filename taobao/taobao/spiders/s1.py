# -*- coding: utf-8 -*-
import scrapy
import json,jsonpath
from ..items import TaobaoItem
from datetime import datetime
from urllib import request
from lxml import etree
import datetime

class S1Spider(scrapy.Spider):
    name = 's1'
    allowed_domains = ['taobao.com']
    start_urls = []
    base_url = 'https://s.m.taobao.com/search?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&q=%E7%99%BD%E9%85%92&sst=1&n=20&buying=buyitnow&m=api4h5&token4h5=&abtest=18&wlsort=18&page='

    for i in range(1, 2, 1):
        url = base_url + str(i)
        start_urls.append(url)

    def parse(self, response):
        content = response.body.decode('utf-8')
        ##使用jsonpath之前，将json格式转换为标准的python格式
        data_dict = json.loads(content)
        listitem = jsonpath.jsonpath(data_dict, '$..listItem.*')
        for product in listitem:
            p = TaobaoItem()
            title = product['title']
            p['title'] = title
            price = product['price']
            p['price'] = price
            originalPrice = product['originalPrice']
            p['originalPrice'] = originalPrice
            sold = product['sold']
            p['sold'] = sold
            sellerLoc = product['sellerLoc']
            p['sellerLoc'] = sellerLoc
            nick = product['nick']
            p['nick'] = nick
            url = product['url']
            p['url'] = url
            p['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            ##路径拼接：
            new_url = request.urljoin(response.url, url)

            ##封装请求的：
            scrapy.Request(url=new_url, callback=self.detail_parse, meta={'data': p, 'phantoms': True})

    def detail_parse(self,response):
        # print('######')

        p = response.request.meta['data']
        content = response.body.decode('utf-8')
        tree = etree.HTML(content)
        ##每月销量：
        try:
            sales=tree.xpath('//span[@class="sales"]/text()')
            p['sales']=sales
        except:
            pass

        yield p
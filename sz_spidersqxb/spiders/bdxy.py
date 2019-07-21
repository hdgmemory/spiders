# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import random
from PIL import Image,ImageEnhance
import locale
locale.setlocale(locale.LC_ALL, 'C')
import tesserocr
import time
import re
from sz_spidersqxb.items import BDXY
from sz_spidersqxb.pipelines import SzSpidersbdxyPipeline
from selenium.webdriver.support import expected_conditions as EC
class BdxySpider(scrapy.Spider):
    name = 'bdxy'
    allowed_domains = ['xin.baidu.com']
    start_urls = ['http://xin.baidu.com/']

    def parse(self, response):

        chrome = webdriver.Chrome()
        i = 0
        S = SzSpidersbdxyPipeline()
        while i < 1000:
            i += 1
            cnames = S.getCompanyName()
            try:
                for item in cnames:
                    time.sleep(random.uniform(2,3))
                    chrome.get('https://xin.baidu.com/')
                    chrome.find_element_by_xpath('//div[@class="index-search-type"]/span[3]').click()
                    time.sleep(random.uniform(2, 3))
                    chrome.find_element_by_xpath('//div[@class="ui-textbox textbox-autocomplete"]/input').send_keys(
                        item)
                    time.sleep(random.uniform(2, 3))
                    chrome.find_element_by_xpath('//div[@class="ui-textbox textbox-autocomplete"]/input').send_keys(
                        Keys.ENTER)
                    time.sleep(random.uniform(1, 2))
                    href = chrome.find_element_by_link_text(item).get_attribute('href')
                    chrome.get(href)

                    # time.sleep(random.uniform(1, 2))
                    text1 = chrome.find_element_by_xpath('//*[@id="basic-wrap"]/div/div[1]/div[1]/p[1]/span').text

                    time.sleep(random.uniform(2, 3))
                    b = BDXY()
                    b['cname'] = item
                    b['uscc'] = text1
                    yield b
            except Exception:
                pass
            continue

# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import random
import time
from sz_spiders.pipelines import TYC_Pipeline
from sz_spiders.items import TYC
class TycSpider(scrapy.Spider):
    name = 'tyc'
    allowed_domains = ['tianyancha.com']
    start_urls = ['http://tianyancha.com/login?from=https%3A%2F%2Fwww.tianyancha.com%2Fcompany%2F2464936087']

    def parse(self, response):
        # content = response.body.decode('utf-8')
        # tree = etree.HTML(content)
        chrome = webdriver.Chrome()
        chrome.get('https://www.tianyancha.com/login?from=https%3A%2F%2Fwww.tianyancha.com%2Fcompany%2F2464936087')
        time.sleep(3)
        chrome.find_element_by_xpath('//div[@class="title-tab text-center"]/div[@class="title"]').click()
        chrome.find_element_by_xpath('//div[@class="modulein modulein1 mobile_box  f-base collapse in"]/div[@class="pb30 position-rel"]/input[@class="input contactphone"]').send_keys(username)
        chrome.find_element_by_xpath('//input[@class="input contactword input-pwd"]').send_keys(password)
        chrome.find_element_by_xpath('//div[@class="modulein modulein1 mobile_box  f-base collapse in"]/div[@class="btn -hg btn-primary -block"]').click()
        i = 0
        T = TYC_Pipeline()
        while i < 5000:
            i += 1
            cnames = T.getCompanyName()
            time.sleep(1)
            for item in cnames:
                time.sleep(random.uniform(1, 2))
                chrome.find_element_by_xpath('//input[@id="header-company-search"]').clear()
                chrome.find_element_by_xpath('//input[@id="header-company-search"]').send_keys(item)
                time.sleep(random.uniform(0.5,1))
                try:
                    chrome.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div').click()
                    a = chrome.find_element_by_xpath(
                        '//*[@id="web-content"]/div/div[1]/div[4]/div[2]/div/div/div[3]/div[1]/a')
                    href = a.get_attribute('href')
                    chrome.get(href)

                    text1 = chrome.find_element_by_xpath(
                        '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]').text
                    # print(item, ',', text1)
                    # T.saveData(item.strip(), text1)
                    u = TYC()
                    u['uscc'] = text1
                    u['cname'] = item
                    yield u
                except Exception:
                    pass
                continue
        chrome.close()
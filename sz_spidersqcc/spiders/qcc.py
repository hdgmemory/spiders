# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import time
from sz_spidersqcc.pipelines import QccPipeline
from sz_spidersqcc.items import QCC
class QccSpider(scrapy.Spider):
    name = 'qcc'
    allowed_domains = ['qichacha.com']
    start_urls = ['http://qichacha.com/']

    def parse(self, response):
        chrome_options = Options()
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel …) Gecko/20100101 Firefox/61.0"')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chrome = webdriver.Chrome(executable_path='/Users/explore/Developments/chromedriver/chromedriver')
        chrome = webdriver.Chrome()
        chrome.get('https://www.qichacha.com/user_login?back=%2Ffirm_CN_59a1bc8739127dff9ea7e58a8280c4ae.html')

        # time.sleep(3)
        # chrome.find_element_by_xpath('//*[@id="normalLogin"]').click()
        # chrome.find_element_by_xpath('//*[@id="nameNormal"]').send_keys(username)
        # chrome.find_element_by_xpath('//*[@id="pwdNormal"]').send_keys(password)
        #
        # chrome.find_element_by_xpath('//*[@id="user_login_normal"]/button').click()
        time.sleep(30)
        i = 0
        Q = QccPipeline()
        while i < 5000:
            i += 1
            cnames = Q.getCompanyName()
            chrome.get('https://www.qichacha.com/search?key=%E4%B8%8A%E6%B5%B7%E9%92%A7%E6%AD%A3%E7%BD%91%E7%BB%9C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8')
            for item in cnames:
                try:
                    #time.sleep(random.uniform(1, 3))
                    chrome.find_element_by_xpath('//*[@id="headerKey"]').clear()
                    # chrome.find_element_by_xpath('//*[@id="headerKey"]').send_keys(item)
                    # #time.sleep(random.uniform(2, 4))
                    # chrome.find_element_by_xpath('/html/body/header/div/form/div/div/span/button').click()
                    # href = chrome.find_element_by_xpath('//*[@id="search-result"]/tr[1]/td[3]/a').get_attribute('href')
                    chrome.find_element_by_xpath('//input[@id="headerKey"]').send_keys(item)
                    chrome.find_element_by_xpath('//button[@class="btn btn-primary top-searchbtn"]').click()
                    href = chrome.find_element_by_xpath('//a[@class="ma_h1"]').get_attribute('href')
                    chrome.get(href)
                    text1 = chrome.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[2]').text
                    # print(item, ',', text1)
                    # Q.saveData(item.strip(), text1)
                    q = QCC()
                    q['text'] = text1
                    q['name'] = item
                    yield q
                except Exception:
                    pass
                continue
        chrome.close()
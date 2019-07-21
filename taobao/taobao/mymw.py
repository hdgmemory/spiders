from selenium import webdriver
from scrapy.http.response.html import HtmlResponse
import time
class TaobaoDownloaderMiddleware(object):

    def __init__(self):
        self.browser = webdriver.PhantomJS(r'/Users/hdg/phantomjs/bin/phantomjs')

    def process_request(self, request, spider):

        ##详情页使用无界面进行访问：如若请求里面附带了phantoms这样的参数，那么走中间键进行请求：
        if request.meta.get('phantoms',False):
            self.browser.get(request.url)
            time.sleep(3)
            content = self.browser.page_source##响应信息

            ##将信息封装成response对象，传给回调函数：
            response=HtmlResponse(url=request.url,encoding='utf-8',body=content,request=request)

            return response
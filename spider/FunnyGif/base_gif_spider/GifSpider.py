#!/usr/bin/env python
# -*-coding:utf-8-*-
from lxml import html
import requests


class BaseGifSpider(object):
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.google.com",
               "User-Agent": ":Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
               }

    def __init__(self, pageUrl, charset='utf-8'):
        self.pageUrl = pageUrl
        self.charset = charset
        pass

    def request(self,pageUrl = ''):
        if  len(pageUrl) == 0:
            pageUrl = self.pageUrl
        print 'request = ' + pageUrl
        if pageUrl is None or len(pageUrl) == 0:
            return None
        page = requests.get(pageUrl, headers=self.headers)
        page.encoding = self.charset
        if page.status_code == 200:
            tree = html.fromstring(page.text)
            return tree
        return None

    #获取主界面的所有子页面URL集合
    def getTotalPageList(self):
        pass
    #获取详情页所遇子页面URL集合
    def requestChildPageList(self):
        pass
    # www.xxx.com ----> xxx
    def getPageDomain(self):
        self.pageUrl.split('')
        pass


    def startRequest(self,reverse=False):
        pass

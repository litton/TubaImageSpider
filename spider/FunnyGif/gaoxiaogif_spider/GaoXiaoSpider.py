#!/usr/bin/env  python
# -*-coding:utf-8-*-
from lxml import html
import requests
from base_gif_spider.GifSpider import BaseGifSpider
from base_gif_spider.Items import GifItem
from db.DBHelper import DBHelper
import re
import string


class GaoXiaoGifSpider(BaseGifSpider):
    def __init__(self):
        self.pageUrl = "http://www.gaoxiaogif.com/all/"
        self.domain = 'http://www.gaoxiaogif.com'
        BaseGifSpider.__init__(self, self.pageUrl, charset='gb2312')
        self.dbHelper = DBHelper()

    def getTotalPageList(self):
        page_list = [self.pageUrl]
        tree = super(GaoXiaoGifSpider, self).request()
        hrefXhs = tree.xpath('//div[@class="page"]/a/@href')
        if hrefXhs is not None and len(hrefXhs) > 0:
            lasthref = hrefXhs[len(hrefXhs) - 1]
            if lasthref:
                array = lasthref.split("_")
                if len(array) > 1:
                    pageInfo = array[1].split(".")[0]
                    count = int(pageInfo)
                    url_template = 'http://www.gaoxiaogif.com/all/index_%d.html'
                    for index in range(2, 1 + count):
                        url = url_template % (index)
                        page_list.append(url)

        return page_list

    def parseCategoryPage(self, url):
        tree = super(GaoXiaoGifSpider, self).request(url)
        detail_page_url_list = []
        if tree is not None:
            xhs = tree.xpath('//div[@class="likepage"]/ul/li')
            if xhs is not None and len(xhs) > 0:
                for index in range(2, 1 + len(xhs)):
                    srcXhs = tree.xpath('//div[@class="likepage"]/ul/li[%d]//a[@title]/@href' % index)
                    if srcXhs is not None and len(srcXhs) > 0:
                        href = srcXhs[0]
                        if href.endswith('.html'):
                            url = href
                            if not href.startswith('http:'):
                                url = self.domain + href
                            detail_page_url_list.append(url)
        return detail_page_url_list

    def parseGifDetailPage(self, url):
        tree = super(GaoXiaoGifSpider, self).request(url)
        titleXhs = tree.xpath('//div[@class="listgif-title"]//h1/text()')
        if titleXhs is not None and len(titleXhs) > 0:
            title = self.formatChinese(titleXhs[0])
            srcXhs = tree.xpath('//div[@class="listgif-giftu content_pic"]//img/@src')
            if srcXhs is not None and len(srcXhs) > 0:
                for index in range(0,len(srcXhs)):
                    gif_url = srcXhs[index]
                    if gif_url.endswith('.gif'):
                        item = GifItem()
                        item.gif_url = gif_url
                        item.gif_title = title
                        self.dbHelper.saveGifItem(item)

    def formatChinese(self, title):
        return title.encode('utf-8')

    def startRequest(self,reverse=False):
        category_list = self.getTotalPageList()
        if reverse:
            #逆序抓取
            for i in range(len(category_list)):
                item = category_list[len(category_list) -i -1]
                detail_urls = self.parseCategoryPage(item)
                for index in range(len(detail_urls)):
                    url = detail_urls[len(detail_urls) - index - 1]
                    self.parseGifDetailPage(url)
        else:
            for item in category_list:
                detail_urls = self.parseCategoryPage(item)
                for url in detail_urls:
                    self.parseGifDetailPage(url)
      #  for item in category_list:



if __name__ == "__main__":
    spider = GaoXiaoGifSpider()
    # spider.parseCategoryPage("http://www.gaoxiaogif.com/all/index_282.html")
    #spider.parseGifDetailPage('http://www.gaoxiaogif.com/dongwugif/8084.html')
    spider.startRequest()
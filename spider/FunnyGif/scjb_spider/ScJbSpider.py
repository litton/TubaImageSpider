#!/usr/bin/env  python
# -*-coding:utf-8-*-
from lxml import html
import requests
from base_gif_spider.GifSpider import BaseGifSpider
from base_gif_spider.Items import GifItem
from db.DBHelper import DBHelper
import re
import string


class ScJbSpider(BaseGifSpider):
    def __init__(self):
        self.pageUrl = "http://sc.jb51.net/gaoxiaotupian/"
        self.domain = 'http://sc.jb51.net'
        BaseGifSpider.__init__(self, self.pageUrl, charset='gb2312')
        self.dbHelper = DBHelper()

    def startRequest(self):
        request_list = self.getTotalPageList()
        for item in request_list:
            list = self.startRequestCategoryList(item)
            for item in list:
                detail_list = self.requestChildPageList(item)
                for url in detail_list:
                    self.requestDetailPage(url)

    def startRequestCategoryList(self, url):
        tree = super(ScJbSpider, self).request(url)
        if tree is not None:
            target_list = []
            xhs = tree.xpath('//div[@class="all_list"]/ul/li')
            if xhs:
                length = len(xhs)
                for index in range(1, length + 1):
                    hrefXhs = tree.xpath('//div[@class="all_list"]/ul/li[%d]/a/@href' % index)
                    if hrefXhs is not None and len(hrefXhs) > 0:
                        target_list.append(self.domain + hrefXhs[0])
            return target_list

    def formatChinese(self, title):
        return title.encode('utf-8')

    def getTotalPageList(self):
        page_list = [self.pageUrl]
        tree = super(ScJbSpider, self).request()
        if tree is not None:
            nextPagesXhs = tree.xpath('//div[@class="pagelist"]//span[@class="pageinfo"]/strong[1]/text()')
            if nextPagesXhs:
                pageInfo = self.formatChinese(nextPagesXhs[0])
                prefix = self.pageUrl + 'list_%s.html'
                if re.match("\d+", pageInfo):
                    for index in range(2, 1 + int(pageInfo)):
                        url = prefix % (str(index))
                        page_list.append(url)
        return page_list

    def requestDetailPage(self, page_url):
        tree = super(ScJbSpider, self).request(page_url)
        if tree is not None:
            xhs = tree.xpath('//div[@class="content-c2"]')
            if xhs:
                srcXhs = tree.xpath('//div[@class="content-c2"]//p[count(*)=1]/img/@src')  # 选择所有p子节点为1的下面的img的href
                #titleXhs = tree.xpath('//div[@class="content-c2"]//p[not(self::text()[not(normalize-space())])]/text()')
                titleXhs = tree.xpath('//div[@class="content-c2"]//p[string-length(text()) > 0]/text()')
                title_list = []
                if titleXhs is not None and len(titleXhs):
                      for i in range(0,len(titleXhs)):
                           title =self.formatChinese(titleXhs[i]).translate(string.maketrans("\n\t\r", "   ")).strip()
                           if  len(title) > 0:
                               title_list.append(title)

                if srcXhs is not None and len(srcXhs) > 0:
                    if  len(title_list) > 0:
                        titleLength = len(title_list)
                        for index in range(0, len(srcXhs)):
                            href = srcXhs[index]
                            if not href.startswith("http:"):
                                href = self.domain + href

                            if href.endswith('.gif'):
                                if index < titleLength:
                                    if self.isGifUrlAvailable(href):
                                        item = GifItem()
                                        item.gif_url = href
                                        item.gif_title = title_list[index]
                                        self.dbHelper.saveGifItem(item)

    def isGifUrlAvailable(self,gifUrl):
        return super(ScJbSpider,self).isGifUrlAvailable(gifUrl)

    def requestChildPageList(self, page_url):
        child_list = [page_url]
        tree = super(ScJbSpider, self).request(page_url)
        if tree is not None:
            nextPagesXhs = tree.xpath('//div[@class="content-c2"]/div/ul[1]/li[1]/a/text()')
            if nextPagesXhs:
                url = self.formatChinese(nextPagesXhs[0])
                regex = re.compile(r'\S+(\d+)\S+')
                result = regex.findall(url)
                if result:
                    pageCount = int(result[0])
                    url = page_url.split('.htm')[0]
                    for index in range(2, 1 + pageCount):
                       full_url = url + '_' + str(index) + '.htm'
                       child_list.append(full_url)
                       print full_url
        return child_list


if __name__ == "__main__":
    spider = ScJbSpider()
    spider.startRequest()
    #spider.requestDetailPage("http://sc.jb51.net/gaoxiaotupian/167074.htm")
    #spider.requestDetailPage("http://sc.jb51.net/gaoxiaotupian/130937.htm")
    # spider.getTotalPageList()

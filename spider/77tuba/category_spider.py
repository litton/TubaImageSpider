#!/usr/bin/env  python
#-*-coding:utf-8-*-
from lxml import html
import requests
from DiskSaveData import DiskDbHelper
from Items import HotGirlModelItem
from Items import ImgeItems
import re
from DownloadUtil import DownloadFileHelper
class TubaCategorySpider:

    host = 'http://www.77tuba.com'
    def __init__(self,category_url,category_id):
        self.dbHelpder = DiskDbHelper(category_id)
        self.category_url = category_url
        self.category_name = category_id
        self.downloadHelper = DownloadFileHelper()

        pass

    def saveCategoryJson(self,id):
         pass
    def saveDetailJson(self,suffix):
        pass

    def getModelName(self,title):
        array = title.split(' ')
        #print len(array)
        if  array and len(array) > 2:
            return array[-2]
        return title

    def getId(self,title):
        #array = title.split(' ')

        return str(hash(title)).replace('-','')


        #for item in array:
         #   print item
    #抓取图吧所有的类目
    def tubaCategorySpider(self):
        pass
    def detailPageSpider(self,page_url,title,page_index):
        page = requests.get(page_url)
        page.encoding = 'gb2312'
        print page_url
        if page.status_code == 200:
            tree = html.fromstring(page.text)

            xhs = tree.xpath('//ul[@class="file"]//img/@src')
            if xhs:

                img_list = []
                for  index in range(0,len(xhs)):
                     url = xhs[index]
                     if not xhs[index].startswith('http'):
                         url = self.host + url
                     imgs = ImgeItems()
                     imgs.img = url
                     img_list.append(imgs.__dict__)
                     #print url
                     #self.downloadHelper.startDownload(self.category_name + '/' + modelName,url)
                     #self.dbHelpder.writeDetailPage(title, url)
                self.dbHelpder.writeImgDetailJson(id=self.category_name + '_' + self.getId(title) + '_' + str(page_index), img_list=img_list)

    def findNextPage(self,page_url,tree):
        xhs = tree.xpath('//ul[@class="image"]/text()')
        pageInfo = xhs[0].encode('utf-8')
        childUrlList = []
        pattern = re.compile(r'共(\d+)页:\s+',re.S)
        result = pattern.findall(pageInfo)
        if result:
            prefix = page_url.split('.shtml')[-2]
            for index in range(2,int(result[0])+1):
                 childUrlList.append(prefix + '_' + str(index) + '.shtml')

            return childUrlList

    def firstDetailSpider(self,page_url,title):
        page = requests.get(page_url)
        page.encoding = 'gb2312'
        if page.status_code == 200:
            tree = html.fromstring(page.text)
            xhs = tree.xpath('//ul[@class="file"]//img/@src')
            if xhs:

                img_list = []
                for index in range(0, len(xhs)):
                    url = xhs[index]
                    if not xhs[index].startswith('http'):
                        url = self.host + url
                    imgs = ImgeItems()
                    imgs.img = url
                    img_list.append(imgs.__dict__)
                    #self.downloadHelper.startDownload(self.category_name + '/' + modelName,url)
                    #self.dbHelpder.writeDetailPage(title,url)
                self.dbHelpder.writeImgDetailJson(id=self.category_name + '_' + self.getId(title),img_list=img_list)
            nextPageList = self.findNextPage(page_url,tree)
            page_index = 1
            for item in nextPageList:
                self.detailPageSpider(item,title,page_index)
                page_index += 1

    def modelCoverSpider(self,page_index,category_url,category_name):
        print category_url
        dbHelper = DiskDbHelper(category_name)
        page = requests.get(category_url)
        page.encoding = 'gb2312'
        if page.status_code == 200:
            tree = html.fromstring(page.text)

            xhs = tree.xpath('//div[@class="lm"]/table')
            if xhs:
                trXhs = tree.xpath('//div[@class="lm"]/table/tr')

                if trXhs:
                    category_list = []
                    for index in range(1, len(trXhs) + 1):
                        tdXhs = tree.xpath('//div[@class="lm"]/table/tr[%d]/td' % index)
                        if tdXhs:
                            for i in range(1, len(tdXhs) + 1):
                                tableCount = tree.xpath('//div[@class="lm"]/table/tr[%d]/td[%d]/table' % (index, i))
                                if tableCount and len(tableCount) > 1:
                                    child = tree.xpath(
                                        '//div[@class="lm"]/table/tr[%d]/td[%d]/table[1]//a/@href' % (index, i))
                                    if child:
                                        childurl = child[0]
                                        if not childurl.startswith('http'):
                                            childurl = self.host + child[0]
                                        imgHxs = tree.xpath(
                                            '//div[@class="lm"]/table/tr[%d]/td[%d]/table[1]//img/@src' % (index, i))
                                        if imgHxs:
                                            img_url = imgHxs[0]
                                            if not img_url.startswith('http'):
                                                img_url = self.host + imgHxs[0]
                                            titleXhs = tree.xpath(
                                                '//div[@class="lm"]/table/tr[%d]/td[%d]/table[2]//a/text()' % (
                                                index, i))
                                            if titleXhs:
                                                # print childurl
                                                # print img_url
                                                # print titleXhs[0].encode('utf-8')
                                                item = HotGirlModelItem()
                                                item.title = titleXhs[0].encode('utf-8')
                                                item.img = img_url
                                                item.child = childurl
                                                item.id = self.category_name + '_' + self.getId(item.title)
                                                item.name = self.getModelName(item.title)
                                                #dbHelper.saveItem(item)
                                                category_list.append(item.__dict__)
                                                self.firstDetailSpider(childurl, item.title)
                            self.dbHelpder.writeCategoryJson(self.category_name+ '_' + str(page_index),category_list)
                            #del self.category_list[:]

    #抓取具体某一个类目里面的数据
    def startLoadByCategory(self):
        print self.category_url
        dbHelper = DiskDbHelper(self.category_name)
        page = requests.get(self.category_url)
        page.encoding = 'gb2312'
        if page.status_code == 200:
            tree = html.fromstring(page.text)

            srcXhs = tree.xpath('//ul[@class="page"]/a/@href')

            category_suffix = ''
            if srcXhs:
                array = srcXhs[0].split('2.shtml')
                if array:
                    category_suffix = array[0]
            totalPageXhs = tree.xpath('//ul[@class="page"]/text()')


            pageInfo = totalPageXhs[0].encode('utf-8')

            childUrlList = []
            pattern = re.compile(r'\s共(\d+)页/*', re.S)
            result = pattern.findall(pageInfo)
            if result:

                if category_suffix:
                    for pageIndex in range(2,1+int(result[0])):
                         childUrlList.append(self.category_url + category_suffix + str(pageIndex) + '.shtml')

            xhs = tree.xpath('//div[@class="lm"]/table')
            if xhs:
                trXhs = tree.xpath('//div[@class="lm"]/table/tr')

                if trXhs:
                    category_list = []
                    for index in range(1,len(trXhs) +1):
                        tdXhs = tree.xpath('//div[@class="lm"]/table/tr[%d]/td'%index)
                        if tdXhs:

                            for i in range(1,len(tdXhs) + 1):
                                tableCount = tree.xpath('//div[@class="lm"]/table/tr[%d]/td[%d]/table'%(index,i))
                                if tableCount and len(tableCount) > 1:
                                    child = tree.xpath('//div[@class="lm"]/table/tr[%d]/td[%d]/table[1]//a/@href' % (index,i))
                                    if child:
                                        childurl = child[0]
                                        if not childurl.startswith('http'):
                                            childurl = self.host + child[0]
                                        imgHxs = tree.xpath('//div[@class="lm"]/table/tr[%d]/td[%d]/table[1]//img/@src' % (index, i))
                                        if imgHxs:
                                             img_url = imgHxs[0]
                                             if not img_url.startswith('http'):
                                                img_url = self.host + imgHxs[0]
                                             titleXhs = tree.xpath('//div[@class="lm"]/table/tr[%d]/td[%d]/table[2]//a/text()'% (index, i))
                                             if titleXhs:
                                                item  = HotGirlModelItem()
                                                item.title = titleXhs[0].encode('utf-8')
                                                item.img = img_url
                                                item.child = childurl
                                                item.id = self.category_name + '_' + self.getId(item.title)
                                                item.name = self.getModelName(item.title)

                                                #dbHelper.saveItem(item)
                                                category_list.append(item.__dict__)
                                                self.firstDetailSpider(childurl,item.title)
                    self.dbHelpder.writeCategoryJson(self.category_name,category_list)
                    #del self.category_list[:]
            #递归爬取下一页的数据
            if childUrlList:
                print len(childUrlList)
                page_index = 1
                for item in childUrlList:
                    self.modelCoverSpider(page_index,item,self.category_name)
                    page_index +=1



if __name__ == '__main__':
    spider = TubaCategorySpider("http://www.77tuba.com/1021/","1021")
    spider.startLoadByCategory()
    #spider.saveCategoryJson('1021')


    #print  spider.getId('[ugirls尤果]No.243 施诗 换上制服媚眼含羞纤长美腿')
    #print  spider.getId('[DISI第四印象]NO.716 蓝色紧身长裤窈窕纤细秀美背')
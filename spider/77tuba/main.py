#!/usr/bin/env python
#-*-coding:utf-8-*-
import threading
import thread
from category_spider import TubaCategorySpider


def startSpider(url,category_name):
    thread1 = threading.Thread(target=doWork,args=(url,category_name))
    thread1.start()





def doWork(url,category_name):
    print threading.currentThread().getName()
    spider = TubaCategorySpider(url,category_name)
    spider.startLoadByCategory()




if __name__ == '__main__':
    print 'start tuba spider action'
    startSpider('http://www.77tuba.com/1040/','ugirl')
    #startSpider('http://www.77tuba.com/1062/', '10')
    #startSpider('http://www.77tuba.com/1047/', 'siya')
    print 'finish tuba spider action'
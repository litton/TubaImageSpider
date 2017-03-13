#!/usr/bin/env  python
#-*-coding:utf-8-*-
from scjb_spider.ScJbSpider import ScJbSpider
from base_gif_spider.GifSpider import BaseGifSpider





if __name__ == "__main__":
    spider = ScJbSpider()
    spider.startRequest()
    print '抓取完成'




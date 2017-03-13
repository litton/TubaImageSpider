#!/usr/bin/env python
# -*-coding:utf-8-*-
import MySQLdb

from base_gif_spider.Items import GifItem
from base_gif_spider.Const import GLOBAL_GIF_TABLE
import time
import base64
import datetime


class DBHelper(object):
    create_gif_sql = 'insert into ' + GLOBAL_GIF_TABLE + ' (gif_title,gif_url,gif_id,create_time_stamp) values ("%s","%s","%s","%s");'
    query_gif_sql = "select * from " + GLOBAL_GIF_TABLE + " where gif_url = '%s'  "
    query_gif_limit_sql = "select * from " + GLOBAL_GIF_TABLE +  " order by create_time_stamp asc limit %s,%s"
    delete_gif_sql = "delete from " + GLOBAL_GIF_TABLE + " where gif_url = '%s' "
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='fanlitao',
        passwd='123456',
        db='funny_gif',
    )

    def __init__(self):
        pass

    def saveGifItem(self, gifItem):
        try:
            cursor = self.conn.cursor()
            sql = self.create_gif_sql % (gifItem.gif_title, gifItem.gif_url,self.getGifId(gifItem.gif_url), self.getNow())
            print sql
            cursor.execute(sql)

            self.conn.commit()

        except Exception,ex:
            print 'dont insert duplicate ',ex

    def getNow(self):
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        return now

    def getGifId(self,key):
        return  base64.encodestring(key)


    def getGifItemByUrl(self,url):
        cursor = self.conn.cursor()
        query_url = self.query_gif_sql % (url)
        try:
            print query_url
            count = cursor.execute(query_url)
            if count > 0:
                result = cursor.fetchone();
                if result:
                    item = GifItem()
                    item.gif_title = result[1]
                    item.gif_url = result[2]
                    item.gif_timestamp = result[9]
                    return item
        except Exception,ex:
           print ex


    def convertCursor2Item(self,results):
        items = []
        for row in results:
            item = GifItem()
            item.gif_title = row[1]
            item.gif_url = row[2]
            #item.gif_timestamp = row[9]
            items.append(item.__dict__)

        return items





    def getGifItemsLimit(self,start,end):
        cursor = self.conn.cursor()
        url = self.query_gif_limit_sql%(start,end)
        count = cursor.execute(url)
        results = cursor.fetchall()
        return self.convertCursor2Item(results)


    def deleteGifItemByUrl(self,url):
        cursor = self.conn.cursor()
        query_url = self.delete_gif_sql % (url)
        print query_url
        count = cursor.execute(query_url)
        if count > 0:
            return True

        return False


if __name__ == '__main__':
    # item = GifItem
    # item.gif_title = "刚被人从陷阱里解救出来，在外放生…… 结果回到大自然还不到5秒…. 又钻进了人类的陷阱里…"
    # item.gif_url = "http://scimg.jb51.net/allimg/170312/2-1F312113212160.gif"
    helper = DBHelper()
    helper.getGifItemsLimit(0,10);
    #helper.saveGifItem(item)
    #item2 = helper.getGifItemByUrl("http://scimg.jb51.net/allimg/170308/2-1F30R13535444.gif")
    #print item2
    #result = helper.deleteGifItemByUrl('http://scimg.jb51.net/allimg/170308/2-1F30R13535444.gif')
    #print result
#!/user/bin/env python
#-*-coding:utf-8-*-

import MySQLdb as mydb
import db.DBHelper as dbHelper
from base_gif_spider.Const import GLOBAL_GIF_TABLE
from base_gif_spider.Const import  GLOBAL_GIF_COMMENT_TABLE
class CreateDBHelper(object):



    def __init__(self):
        self.connect = mydb.connect(host='localhost',
        port = 3306,
        user='fanlitao',
        passwd='123456',
        db ='funny_gif',)
        pass

    def createDB(self):
        pass


    def dropAllTable(self):
        cursor = self.connect.cursor()
        drop_table = "drop table " + GLOBAL_GIF_TABLE
        cursor.execute(drop_table)

        cursor.execute("drop table " + GLOBAL_GIF_COMMENT_TABLE)

        self.connect.commit()

    def createGifTable(self):
        cursor = self.connect.cursor()

        gif_main_table_sql = "CREATE TABLE  if not exists " + GLOBAL_GIF_TABLE +" (id int UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,\
        gif_title varchar(255),gif_url  varchar(512) not null UNIQUE ,type int,\
        gif_id varchar(255) not null,\
         like_info int unsigned default 0, unlike_info int unsigned default 0,\
         quality tinyint default 0, gif_flag tinyint unsigned default 0 ,\
         create_time_stamp timestamp)"

        print gif_main_table_sql

        cursor.execute(gif_main_table_sql)


        create_comment_sql = "create table if not exists " + GLOBAL_GIF_COMMENT_TABLE +" (id int unsigned not null primary key auto_increment,gif_id varchar(255) not null ,author varchar(20), \
                             content text not null,create_time_stamp timestamp)"

        cursor.execute(create_comment_sql)

        self.connect.commit()
        pass

    #修改存储中文信息字段的字符集
    def alterTableDefaultCharset(self):
        cursor = self.connect.cursor()
        change_gif_charset = "ALTER TABLE " +GLOBAL_GIF_TABLE+" CHANGE gif_title gif_title varchar(255) CHARACTER SET utf8mb4"
        cursor.execute(change_gif_charset)

        change_comment_charset = "ALTER TABLE "+ GLOBAL_GIF_COMMENT_TABLE+" CHANGE content content text CHARACTER SET utf8mb4"
        self.connect.commit()

    #关闭连接
    def close(self):
        self.connect.close()




if __name__ == '__main__':

    cdb = CreateDBHelper()
    cdb.createGifTable();
    cdb.close()
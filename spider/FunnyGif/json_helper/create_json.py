#!/usr/bin/env  pytho
#-*-coding:utf-8-*-
from db.DBHelper import  DBHelper
from base_gif_spider.Items import GifItem
import json
import os
class CreateJsonHelper:


    def __init__(self):
        self.db = DBHelper()
        pass

    def writeGifJson(self, gif_list):
        print len(gif_list)

        response_result = {'status': '200'}
        response_result['data'] = gif_list

        json_content = json.dumps(response_result)
        name = '../../gif_api/gif_main.json'
        if os.path.exists(name):
            os.remove(name)
        print name
        output = open(name, 'w')
        output.write(json_content)
        output.flush()
        output.close()

    def writeOkResultJson(self):
        response_result = {'status': '200'}
        name = '../../gif_api/sucess.json'
        output = open(name, 'w')
        output.write(json.dumps(response_result))
        output.flush()
        output.close()

    def writeJson(self):
        items = self.db.getGifItemsLimit(4500,4800)
        self.writeGifJson(items)





helper = CreateJsonHelper()
helper.writeJson()
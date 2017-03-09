#!/usr/bin/env python
#-*-coding:utf-8-*-
import os
import json
from Items  import HotGirlModelItem
class DiskDbHelper(object):


    def __init__(self,dbname):
        self.db = dbname + '.html'
        self.path = os.getcwd() + '/dir_' + dbname

        if not os.path.exists('api'):
            os.mkdir('api')
        self.json_base = 'api/' + dbname
        self.category = self.json_base + '/category'
        self.img = self.json_base + '/img'
        if not os.path.exists(self.json_base):
            os.mkdir(self.json_base)
        if not os.path.exists(self.category):
            os.mkdir(self.category)
        if not os.path.exists(self.img):
            os.mkdir(self.img)



    def saveItem(self,item):
        content = "<div><a href='" + item.child + "'><img src='" + item.img+"'/></a></div>"
        self.writeLine(content)


    def writeLine(self,content):
        if os.path.exists(self.db):
            output = open(self.db,'a+')
            output.write(content)
            output.write('\n')
            output.flush()
            output.close()
        else:
            output = open(self.db,'w')

            output.write("<html><head><title>PythonWebService </title></head ><body>")
            output.write(content)
            output.write('\n')
            output.flush()
            output.close()



    def writeDetailPage(self,title,line):
        file = self.path +'/' + title + '.txt'
        if os.path.exists(file):
            output = open(file, 'a+')
            output.write(line)
            output.write('\n')
            output.flush();
            output.close()
        else:
            output = open(file, 'w')
            output.write(line)
            output.write('\n')
            output.flush()
            output.close()

    def writeCategoryJson(self,id,category_list):
        response_result = {'status':'200'}
        response_result['data'] = [category_list]
        json_content = json.dumps(response_result)
        name = self.category + '/' + 'category_' + id + '.json'
        output = open(name, 'w')
        output.write(json_content)
        output.flush()
        output.close()
        #print json_content

    def writeImgDetailJson(self,id,img_list):
        if img_list and len(img_list) > 0:
            print id
            response_result = {'status': '200'}
            response_result['data'] = [img_list]
            json_content = json.dumps(response_result)
            name = self.img + '/' + id + '.json'
            output = open(name, 'w')
            output.write(json_content)
            output.flush()
            output.close()
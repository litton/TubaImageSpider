#!/usr/bin/env python
#-*-coding:utf-8-*-
import os
import json
from Items  import HotGirlModelItem
class DiskDbHelper(object):


    def __init__(self,dbname):
        self.db = dbname + '.html'
        self.path = os.getcwd() + '/dir_' + dbname
        self.json_base = dbname

        if not os.path.exists(self.json_base):
            os.mkdir(dbname)

        if not os.path.exists(self.path):
             os.mkdir(self.path)


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
        name = self.json_base + '/' + 'category_' + id + '.json'
        output = open(name, 'w')
        output.write(json_content)
        output.flush()
        output.close()
        #print json_content

    def writeImgDetailJson(self,id,img_list):
        if img_list and len(img_list) > 0:
            response_result = {'status': '200'}
            response_result['data'] = [img_list]
            json_content = json.dumps(response_result)
            name = self.json_base + '/' + id + '.json'
            output = open(name, 'w')
            output.write(json_content)
            output.flush()
            output.close()
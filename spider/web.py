import os
import sys
import SimpleHTTPServer
import BaseHTTPServer
import threading

import time
import base64
import datetime
import MySQLdb

class DBHelper(object):
	set_expire_url_sql = "update gif_table set gif_flag =1 where gif_url = '%s' "
	conn = MySQLdb.connect(
        	host='localhost',
        	port=3306,
        	user='fanlitao',
        	passwd='123456',
        	db='funny_gif',
    		)
	def __init__(self):
		pass

	def setGifUrlExpireFlag(self, url):
		cursor = self.conn.cursor()
		update_url = self.set_expire_url_sql % (url)
		print update_url
		count = cursor.execute(update_url)
		self.conn.commit()
		print count


class MyHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.redirect():
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_HEAD(self):
        if not self.redirect():
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_HEAD(self)

    def redirect(self):
        path = self.translate_path(self.path)
		
	print path
	print self.path
	array = self.path.split('/')
	print array
	if array[1] == 'gif_api':
		#gif_api/delete?url=xxxx
	      if array[2].startswith('delete'):
		  array =  self.path.split('?')
		  print array
		  if len(array) > 1:
		     url = array[1]
		     url = url.split('=')[1]
             	     if url is not None:
		        dbHelper = DBHelper()
                	dbHelper.setGifUrlExpireFlag(url)
 			self.send_response(302)
			self.send_header("Location",'/gif_api/sucess.json')
			self.end_headers()
			return True
        if os.path.isdir(path):
            for base in "index", "default":
                for ext in ".html", ".htm", ".txt":
                    index = base+ext
                    index_path = os.path.join(path, index)
                    if os.path.exists(index_path):
                        new_path = self.path
                        if not new_path.endswith('/'):
                            new_path += '/'
                        new_path += index

                        self.send_response(302)
                        self.send_header("Location", new_path)
                        self.end_headers()
                        return True
        return False

def test(HandlerClass = MyHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()


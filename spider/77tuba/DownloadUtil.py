#!/usr/bin/env python
#-*-coding:utf-8-*-
from ProgressBar import ProgressBar
import requests
import os


class DownloadFileHelper(object):


    def __init__(self):
        pass


    def startDownload(self,category,url):
        file_name = url.split('/')[-1]
        response = requests.get(url)
        if response.status_code == 200:
            if not os.path.exists(category):
                os.mkdir(category)
            f = open(category + '/' + file_name, 'wb')
            chunk_size = 1024  # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 内容体总
            progress = ProgressBar(file_name, total=content_size,
                                   unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
            for chunk in response.iter_content(chunk_size=512 * 1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    progress.refresh(count=len(chunk))
            response.close()



if __name__ == '__main__':
    downloadFile = DownloadFileHelper()
    downloadFile.startDownload('http://img.77tuba.com/upimgs/allimg/151122/11ZG121G.jpg')





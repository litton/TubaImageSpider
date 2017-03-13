#!/usr/bin/env python
#-*-coding:utf-8-*-



class GifItem(object):


    def __init__(self):
        self.gif_title = ''
        self.gif_url = ''
        # self.gif_id = ''
        # self.gif_timestamp =''

    def __get__(self, obj, type=None):
        return 'get', self, obj, type

    def __set__(self, obj, val):
        print 'set', self, obj, val






class CommentItem(object):


    def __init__(self):
        pass


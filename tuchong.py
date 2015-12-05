# -*- coding: utf-8 -*-  
#!/usr/bin/python
import sys
import urllib2
import re
import os
from core import *

class tuchong():
    def __init__(self):
        self.url = "http://garasu.tuchong.com/"

    def get_imglist(self,data):
        imglist = re.findall('(?<=<img src=")http\S+(?=" class=")',data);
        return imglist;

    def get_timetable(self,data):
        regex = self.url.rstrip("/") + "/posts/20\d\d-\d\d"
        p = re.compile(regex)
        return list(set(p.findall(data))) #remove dup


    def get_detail(self,data):
        regex = self.url.rstrip("/") + '/\d+/"\stitle=".*">'
        title = re.findall(regex,data);
        return title;

    def run(self):
        data = get_page_source(self.url)
        self.timetable_list = self.get_timetable(data)
        for a in range(len(self.timetable_list)):
            data = get_page_source(self.timetable_list[a])
            _bloglist = self.get_detail(data)
            bloglist = []
            for i in range(len(_bloglist)):
                s = []
                v = _bloglist[i]
                s.append(v.split('"')[2])
                s.append(v.split('"')[0])
                bloglist.append(s)
            for i in range(len(bloglist)):
                s = get_page_source(bloglist[i][1])
                l = self.get_imglist(s)
                bloglist[i].pop(1)
                for j in range(len(l)):
                    bloglist[i].append(l[j])
                print bloglist
                print "==="





if __name__ == "__main__":
    test = tuchong()
    test.run()

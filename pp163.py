# -*- coding: utf-8 -*-
#!/usr/bin/python

from core import *

class pp163:
    def __init__(self,author):
        self.author = author;
        self.link = "http://" + author + ".pp.163.com";

    def get_entryurl(self):
        entry = re.findall('(?<=<a href=")http\S+html(?=" title=")',self.home);
        entry = list(set(entry));
        return entry;

    def get_entry_name(self):
        title = re.findall("(?<=title>).*(?=</title)",self.data);
        return title;

    def get_imgurl(self):
        imgurl = re.findall("(?<=data-lazyload-src=\")http\S+.jpg(?=\"\sonerror)",self.data);
        return imgurl;

    def run(self):
        result = []
        self.home = get_page_source(self.link)
        self.entry = self.get_entryurl()
        for i in self.entry:
            self.data = get_page_source(i)
            self.imgurl = self.get_imgurl()
            self.title = self.get_entry_name()
            _res = self.title + self.imgurl
            result.append(_res)
        return result

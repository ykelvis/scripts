# -*- coding: utf-8 -*-
#!/usr/bin/python
import urllib2
import re
import os
import sys

def get_page_source(url):
    req_header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Charset':'utf-8',
            }
    req = urllib2.Request(url,None,req_header);
    try:
        data = urllib2.urlopen(req).read();
    except:
        print "Error loading: ",url
    return data;

def download_img(title,link,path):
    name = re.findall('(?<=/)\d+.jpg',link);
    save_path = unicode(path + "/" + title.decode('gbk'));
    file_path = save_path + "/" + name[0];
    try:
        os.makedirs(path + "/" + title.decode('gbk'));
    except:
        pass;
    if os.path.isfile(file_path):
        print "Already downloaded";
    else:
        try:
            image_data = get_page_source(link);
            image = open(file_path,'wb');
            image.write(image_data);
            image.close();
        except:
            print "Error downloading: ", link, title.decode('gbk');


if __name__ == "__main__":
    from pp163 import *
    
    all = open("lists.txt");
    for a in all:
        author = re.findall("(?<=\/\/).*(?=\.pp)",a)[0]
        path = os.getcwd() + "/" + "pp163" + "/" + author;
        test = pp163(author);
        url_to_img = test.run();
        print "Downloading, " + author;
        for i in range(len(url_to_img)):
            title = url_to_img[i][0]
            for j in range(1,len(url_to_img[i])):
                download_img(title,url_to_img[i][j],path)
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

def get_imgurl(data):
    a = re.findall("(?<=data-lazyload-src=\")http\S+.jpg(?=\"\sonerror)",data);
    return a;

def get_entryurl(data):
    a = re.findall('(?<=<a href=")http\S+html(?=" title=")',data);
    a = list(set(a));
    return a;

def download_img(title,link,path):
    name = re.findall('(?<=/)\d+.jpg',link);
    save_path = unicode(path + "/" + title.decode('gbk'));
    file_path = save_path + "/" + name[0];
    try:
        os.makedirs(path + "/" + title.decode('gbk'));
    except:
        pass;
    try:
        image_data = get_page_source(link);
        image = open(file_path,'wb');
        image.write(image_data);
        image.close();
    except:
        print "Error downloading: ", link, title.decode('gbk');

def get_entry_name(data):
    a = re.findall("(?<=title>).*(?=</title)",data)
    return a;

if __name__ == "__main__":
    _url = sys.argv[1];
    url = "http://" + _url + ".pp.163.com";
    path = sys.argv[2];
    data = get_page_source(url);
    link = get_entryurl(data);
    for i in link:
        page = get_page_source(i);
        entry_title = get_entry_name(page);
        img_link = get_imgurl(page);
        print "Downloading ", entry_title[0].decode('gbk')," ", link.index(i) + 1, " of ", len(link);
        for j in img_link:
            print "Downloading img: ", img_link.index(j) + 1, " of ", len(img_link);
            download_img(entry_title[0],j,path)


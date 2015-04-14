#!/usr/bin/python
import urllib2
import re
import os
import sys

def get_page_source(url):
    data = urllib2.urlopen(url).read();
    return data;

def get_imgurl(data):
    a = re.findall("(?<=data-lazyload-src=\")http\S+.jpg(?=\"\sonerror)",data);
    return a;

def get_entryurl(data):
    a = re.findall('(?<=<a href=")http\S+html(?=" title=")',data);
    a = list(set(a));
    return a;

def download_img(title,link):
    current_dir = os.getcwd();
    name = re.findall('(?<=/)\d+.jpg',link);
    print name;
    save_path = current_dir + "/" + title + "/" + name[0];
    try:
        os.mkdir(current_dir + "/" + title);
    except:
        print "folder exists"
        pass;
    image_data = urllib2.urlopen(link).read();
    image = open(save_path,'wb');
    image.write(image_data);
    image.close();

if __name__ == "__main__":
    _url = sys.argv[1];
    save_dir = sys.argv[2];
    url = "http://" + _url + ".pp.163.com";
    print url;

    data = get_page_source(url);
    link = get_entryurl(data);
    for i in link:
        page = get_page_source(i);
        img_link = get_imgurl(page);
        for j in img_link:
            print j;
            download_img(save_dir,j)

# -*- coding: utf-8 -*-  
#!/usr/bin/python
import sys
import urllib2
import re
import os

def get_page(arg):
    data = urllib2.urlopen(arg).read();
    return data;

def delete_duplicated(arg):
    new_urls = [];
    for url in arg:
        if url not in new_urls:
            new_urls.append(url);
    return new_urls;

def get_imglist(arg):
    imglist = re.findall('http://photos.tuchong.com/\d+/f/\d+.jpg',arg);
    imglist = delete_duplicated(imglist);
    return imglist;

def get_title(arg):
    title = re.findall('(?<=title>).*(?=</title)',arg);
    return title;

def download_img(title,link):
    #current_dir = os.getcwd();
    global path;
    current_dir = path;
    name = re.findall('(?<=/)\d+.jpg',link)
    save_path = current_dir + "/" + title + "/" + name[0];
    print name
    try:
        os.mkdir(current_dir + "/" + title);
    except:
        pass; 
    image_data = urllib2.urlopen(link).read();
    image = open(save_path,'wb');
    image.write(image_data);
    image.close();

if __name__ == "__main__":
    author = sys.argv[1];
    author_link = "http://" + author + ".tuchong.com";
    path = sys.argv[2];
    print author_link;
    page_source = get_page(author_link);
    p = re.compile("http://" + author + ".tuchong.com/\d+/")
    urls = p.findall(page_source);
    print urls;
    urls = delete_duplicated(urls);
    for i in urls:
        blog_source = get_page(i);
        title = get_title(blog_source);
        imglist = get_imglist(blog_source);
        for i in imglist:
            download_img(title[0].decode('utf-8'),i);


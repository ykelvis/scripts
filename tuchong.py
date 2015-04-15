# -*- coding: utf-8 -*-  
#!/usr/bin/python
import sys
import urllib2
import re
import os

def get_page(arg):
    data = urllib2.urlopen(arg).read();
    return data;

def get_all_page_num(arg):
    reg_num = re.compile(ur'(?<=page=)\d(?=">)');
    return reg_num.findall(arg);

def get_imglist(arg):
    imglist = set(re.findall('http://photos.tuchong.com/\d+/f/\d+.jpg',arg));
    return imglist;

def get_title(arg):
    title = re.findall('(?<=title>).*(?=</title)',arg);
    return title;

def get_blog_url(arg):
    p = re.compile(ur'(?<= href=")http://.*tuchong.com/\S+(?=/" target="_blank)')
    urls = p.findall(arg);
    return urls;

def download_img(title,link,path):
    #current_dir = os.getcwd();
    current_dir = path;
    name = re.findall('(?<=/)\d+.jpg',link)
    save_path = current_dir + "/" + title + "/" + name[0];
    print name
    try:
        os.makedirs(current_dir + "/" + title);
    except:
        pass; 
    try:
        image_data = urllib2.urlopen(link).read();
        image = open(save_path,'wb');
        image.write(image_data);
        image.close();
    except:
        print "Error downloading: %s" % link
if __name__ == "__main__":
    link = sys.argv[1];
    path = sys.argv[2];
    ###
    page_source = get_page(link);
    url = get_blog_url(page_source);
    
    page = [1];
    other_page = get_all_page_num(page_source);
    for i in other_page:
        page.append(i);
    
    for i in page:
        link_with_page = link + "/?page=" + str(i);
        page_source = get_page(link_with_page);
        urls = set(get_blog_url(page_source));
        for i in urls:
            blog_source = get_page(i);
            title = get_title(blog_source);
            imglist = get_imglist(blog_source);
            for i in imglist:
                download_img(title[0].decode('utf-8'),i,path);


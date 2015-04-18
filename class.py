#!/usr/bin/python
import re
import urllib2
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
        print "Error loading: ", url;
    return data;

def return_imglist(data,reg_compiled,mode):
    or_list = reg_compiled.findall(data);
    mod_list = [];
    for i in range(len(or_list)):
        if mode == "twitter":
            mod_list.append(or_list[i].replace(":large",":orig"));
        elif mode == "tumblr":
            mod_list.append(or_list[i].replace("_500","_1280"));
    return or_list, mod_list

def download_img(link1,link2,mode,blogger):
    try:
        os.makedirs(mode + "/" + blogger);
    except:
        pass;
    try:
        name = link2.split("/")[-1].replace(":orig","");
        file_path = mode + "/" + blogger + "/" + name;
        try:
            open(file_path);
            print ".",
        except:
            image_data = get_page_source(link2);
            image = open(file_path,'wb');
            image.write(image_data);
            image.close();
            pass;
    except:
        print "Retrying..."
        name = link1.split("/")[-1].replace(":orig","");
        file_path = mode + "/" + blogger + "/" + name;
        try:
            open(file_path);
            print ".",
        except:
            image_data = get_page_source(link1);
            image = open(file_path,'wb');
            image.write(image_data);
            image.close();
            pass

if __name__ == "__main__":
    regx_twitter = re.compile('(?<=data-resolved-url-large=")(http\S+:large)(?=">)');
    regx_tumblr = re.compile('(?<=img src=")(http\S+//\d+.media.tumblr.com/\S+/tumblr_\S+_\S+)(?="/)');

    all_url = open("lists.txt")
    for url in all_url:
        if "twitter" in url:
            mode = "twitter";
            _url = url.split("/")[-2];
            regx = regx_twitter;
        elif "tumblr" in url:
            mode = "tumblr";
            _url = url.split("//")[1].split(".")[0];
            regx = regx_tumblr;
        data = get_page_source(url);
        a,b = return_imglist(data,regx,mode);
        print "Downloading, ", _url;
        for i in range(len(a)):
            try:
                download_img(a[i],b[i],mode,_url);
            except:
                print "Failed, ", a[i]

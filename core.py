# -*- coding: utf-8 -*-
#!/usr/local/bin/python3
from urllib.request import urlopen
import re
import os
import sys

def download_pics(author,title,link):
    save_folder = os.path.join(os.getcwd(),"pics",author,title)
    file_name = re.findall("/(\d+.\w+$)",link)[0]
    try:
        os.makedirs(save_folder);
    except:
        pass;
    if os.path.isfile(os.path.join(save_folder,file_name)):
        print("Already downloaded");
    else:
        try:
            res = urlopen(link);
            image_data = res.read()
            image = open(os.path.join(save_folder,file_name),'wb');
            image.write(image_data);
            image.close();
        except:
            print("Error downloading:{} {} {}".format(link,author,title));

if __name__ == "__main__":
    print('this')

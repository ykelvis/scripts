#!/usr/local/bin/python3
import requests, re
from core import download_pics

class pp163(object):
    def __init__(self,link):
        self.link = link
        self.author = link.split("//")[1].split(".")[0]

    def get_entry(self):
        res = requests.get(self.link).text
        entry = re.findall("http://pp.163.com/{}/pp/\d+.html".format(self.author),res)
        entry = list(set(entry))
        for i in entry:
            r = requests.get(i).text
            title = re.findall("<title>(.*)</title>",r)[0]
            links = re.findall('data-lazyload-src="(.*)" onerror="',r)
            for j in links:
                download_pics(self.author,title,j)

    def run(self):
        self.get_entry()

if __name__ == "__main__":
    all = open("lists.txt")
    for a in all:
        pp163(a).run()

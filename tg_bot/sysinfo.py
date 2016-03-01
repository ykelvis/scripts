#!/usr/local/bin/python3

import os,subprocess
from threading import Thread

class thd(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        a = subprocess.check_output("vnstat -d|tail -3|head -1|awk -F'[|]' '{print $3}'|grep -Eo '\d+.\d+\s\S+'",shell=True)
        _x,y = str(a).split("'")[1].split("\\")[0].split(" ")")")"'")
        x = float(_x)
        if y == "MiB":
            pass
        elif x > 10:
            


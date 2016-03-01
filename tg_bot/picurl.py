#!/usr/local/bin/python3

import requests, re, json, os

def getmain(au):
    a = requests.get('http://{}.pp.163.com/'.format(au)).text
    s = re.findall('http://pp.163.com/{}/pp[^l]*l'.format(au),a)
    _s = list(set(list(s)))
    return _s

def getpic(p):
    global loaded
    r = {}
    for i in p:
        try:
            loaded[i]
        except:
            res = requests.get(i).text
            piclist = re.findall('data-lazyload-src="(\S+)"',res)
            r[i] = piclist
    return r


if os.path.isfile('list.txt'):
    with open('list.txt','r') as f:
        loaded = json.loads(f.read())

with open('lists.txt','r') as _f:
    res = {}
    for line in _f:
        print(line)
        author = re.findall("http://(.*).pp.163.com",line)[0]
        print(author)
        lis = getpic(getmain(author))
        res = dict(res, **lis)

try:
    loaded
    li = dict(res, **loaded)
except:
    li = res

with open('list.txt','w') as f:
    json.dump(li, f, indent=4, sort_keys=True)

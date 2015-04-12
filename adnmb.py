# -*- coding: utf-8 -*-  
#!/usr/bin/python
from datetime import datetime
import json
import re
import urllib2

url = "http://h.koukuko.com";
data = urllib2.urlopen(url).read();

def list_all_borads(arg):
    lists = re.findall("a href=\"(\/[^>]*)>([^<]*)",data);
    for i in range(len(lists)):
        print i,".", lists[i][1]

board_ = u"http://h.koukuko.com/%E7%BB%BC%E5%90%88%E7%89%881.json"
data = urllib2.urlopen(board_).read();

js = json.loads(data)

def convert_datetime(arg):
    arg = arg / 1000;
    result = datetime.fromtimestamp(arg).strftime('%Y-%m-%d %H:%M:%S');
    return result;

def print_color(text,color):
    if color == 0:
        print "\033[1;31;40m%s\033[0m" % text,
    elif color == 1:
        print "\033[1;32;40m%s\033[0m" % text,
    elif color == 2:
        print "\033[1;34;40m%s\033[0m" % text,
    elif color == 3:
        print "\033[1;33;40m%s\033[0m" % text,
    elif color == 4:
        print "\033[1;37;40m%s\033[0m" % text,
    elif color == 5:
        print "\033[0;37;40m%s\033[0m" % text,

def show_board():
    for i in range(len(js['data']['threads'])):
        uid = js['data']['threads'][i]['uid'];
        poster = js['data']['threads'][i]['id'];
        create_time = js['data']['threads'][i]['createdAt'];
        create_time = convert_datetime(create_time);
        content = js['data']['threads'][i]['content'];
        reply = js['data']['threads'][i]['recentReply'];
        print_color(uid,3);
        print_color(poster,2);
        print_color(create_time,1);
        print_color(content,4)
        print "";
        sort_reply = reply[::-1];
        for j in range(len(sort_reply)):
            reply_id = "t" + str(sort_reply[j])
            try:
                reply_uid = js['data']['replys'][reply_id]['uid'];
                reply_iid = js['data']['replys'][reply_id]['id'];
                reply_content = js['data']['replys'][reply_id]['content'];
                reply_time = js['data']['replys'][reply_id]['createdAt'];
                reply_time = convert_datetime(reply_time);
                print "-->",
                if reply_uid == uid:
                    print_color(reply_uid,0);
                else:
                    print_color(reply_uid,3);
                print_color(reply_iid,2);
                print_color(reply_time,1);
                if reply_content[0:24] == '<font color="#789922">>>':
                    print_color(">>",1)
                    print_color(reply_content[24:],5);
                else:
                    print_color(reply_content,5);
                print "";
            except:
                pass;
show_board()

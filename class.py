# -*- coding: utf-8 -*-
#!/usr/bin/python
import urllib2

req_header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Charset':'utf-8',
        }
url = "http://h.koukuko.com";

req = urllib2.Request(url,None,req_header)
resp = urllib2.urlopen(req);
print resp.read()

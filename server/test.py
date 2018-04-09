#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import platform
import requests
import base64
import hashlib

from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding( "utf-8" )

def getStoreRQImageFromServer():
    imageurl = 'image.png'
    rurl = 'https://images-na.ssl-images-amazon.com/images/I/41GUg%2BzzcGL._SL500_AC_SS350_.jpg'
    s = requests.Session()
    s.headers.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
    html = s.get(rurl,verify=False)
    with open(imageurl, 'wb') as file:
        file.write(html.content)
def main():
    pass

def test():
    getStoreRQImageFromServer()

def test2():
    aaa = time.strftime('%Y-%m-%d\n %H:%M:%S',time.localtime(time.time()))
    print(aaa)

#测试
if __name__ == '__main__':
    # main()
    test2()





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
    a = [[1,0],[5,2],[3,1]]
    a.sort(reverse = True)
    print(a)

def test2():
    aaa = time.strftime('%Y-%m-%d\n %H:%M:%S',time.localtime(time.time()))
    print(aaa)


def amazon_price(url, user_agent):
    kv = {'user-agent': user_agent}
    r = requests.get(url, headers = kv)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    atxt = r.text.encode("utf-8")
    # tree = lxml.html.fromstring(r.text.encode("utf-8"))
    # price = tree.cssselect("span#priceblock_ourprice")[0]
    # return price.text_content().encode("gbk")
    f = open('amazon1.html','w')
    f.write(atxt)
    f.close()

def pricetest():
    url = "https://www.amazon.com/dp/B079NP3NMH"
    user_agent = 'Mozilla/5.0'
    amazon_price(url, user_agent)

#测试
if __name__ == '__main__':
    # main()
    test()





#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import platform
import requests
import base64
import hashlib
import dbTool
import json
import random


from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding( "utf-8" )

class BS4HTMLTool(object):
    """docstring for XMLTool"""
    def __init__(self,dtime = 60*60*2):  #默认两小时更新一次数据
        super(BS4HTMLTool, self).__init__()
        self.sysSystem = platform.system()
        if not os.path.exists('img'):
            os.mkdir('img')
        if not os.path.exists('db'):
            os.mkdir('db')

        self.upTime = dtime
        self.dcount = 0
        self.dubDic = {}        #保存所有数据
        self.dbpth = 'db' + os.sep + 'data'
        self.db = dbTool.DBMObj(self.dbpth)
        self.initTool()
        
    def initTool(self):
        self.dubDic = self.db.getDBDatas()     #商品详细内容
        self.dcount = len(self.dubDic.keys())  #保存的商品数量

    def getUrl(self,purl):
        try:
            if purl[0:5] == 'https':
                headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
                res = requests.get(purl, verify=False,headers=headers)
                return res.text
            else:
                headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
                res = requests.get(purl,headers=headers)
                return res.text
        except Exception as e:
            print(e)
        return None
        
    def getImage(self,purl,savename):
        imaexp = purl[purl.rfind('.'):]
        savepth = 'img' + os.sep + savename + imaexp
        try:
            if purl[0:5] == 'https':
                s = requests.Session()
                s.headers.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
                html = s.get(purl,verify=False)
                with open(savepth, 'wb') as file:
                    file.write(html.content)
            else:
                s = requests.Session()
                s.headers.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
                html = s.get(purl)
                with open(savepth, 'wb') as file:
                    file.write(html.content)
            return True
        except Exception as e:
            print(e)
        return False
        
    def getMsgWithURL_eBay(self,purl):
        htmlstr = self.getUrl(purl)
        # f = open('ebay.txt','w')
        # f.write(htmlstr)
        # f.close()
        print('-------eBay---------')
        imgurl = self.findEbayImgURL(htmlstr)
        title = self.findEbayTitle(htmlstr)
        price = self.findEbayPrice(htmlstr)
        base64url = base64.b64encode(purl)
        imgSaveName = hashlib.md5(purl).hexdigest()
        self.getImage(imgurl,imgSaveName)
        outdic = {'imgurl':imgurl,'imgname':imgSaveName,'name':title,'price':price,'time':int(time.time()),'market':'ebay','url':purl}
        
        return outdic

    def findEbayImgURL(self,htmlstr):
        #<meta Property="og:image" Content="https://i.ebayimg.com/images/i/173240166353-0-1/s-l1000.jpg" />
        soup = BeautifulSoup(htmlstr,"html.parser")
        outstr = ''
        for c in soup.head.find_all(name='meta',property='og:image',content=True):
            outstr = c.attrs['content']
            break
        return outstr
    def findEbayTitle(self,htmlstr):
        #/html/head/title
        soup = BeautifulSoup(htmlstr,"html.parser")
        outstr = soup.title.text
        return outstr

    def findEbayPrice(self,htmlstr):
        #<span class="notranslate" id="prcIsum" itemprop="price" style="" content="11.84">US $11.84</span>
        soup = BeautifulSoup(htmlstr,"html.parser")
        outstr = ''
        for c in soup.find_all(name='span',id='prcIsum',itemprop='price'):
            outstr = c.text
        pot = outstr.find('$')
        outstr = outstr[pot:]
        return outstr

    def getMsgWithURL_Amazon(self,purl):
        htmlstr = self.getUrl(purl)
        # f = open('amazon.txt','w')
        # f.write(htmlstr)
        # f.close()
        print('-------Amazon---------')
        imgurl = self.findAmazonImgURL(htmlstr)
        title = self.findAmazonTitle(htmlstr)
        price = self.findAmazonPrice(htmlstr)
        base64url = base64.b64encode(purl)
        imgSaveName = hashlib.md5(purl).hexdigest()
        self.getImage(imgurl,imgSaveName)
        outdic = {'imgurl':imgurl,'imgname':imgSaveName,'name':title,'price':price,'time':int(time.time()),'market':'amazon','url':purl}
        
        return outdic


    def findAmazonImgURL(self,htmlstr):
        #<div id="imgTagWrapperId" class="imgTagWrapper" style="height: 350px;">
        soup = BeautifulSoup(htmlstr,"html.parser")
        outstr = ''
        for c in soup.find_all(name='img',id='comparison_image'):
            outstr = c.attrs['src']
        return outstr

        pass
    def findAmazonTitle(self,htmlstr):
        soup = BeautifulSoup(htmlstr,"html.parser")
        outstr = soup.title.text
        return outstr

    def findAmazonPrice(self,htmlstr):
        #<span id="priceblock_ourprice" class="a-size-medium a-color-price">$7.99</span>
        soup = BeautifulSoup(htmlstr,"html.parser")
        outstr = ''
        for c in soup.find_all(name='span',id='priceblock_ourprice'):
            outstr = c.text
            break
        return outstr

    def getRelUrl(self,dat1,dat2):
        ebay = ''
        amazon = ''
        if dat1[:4] == 'http':
            if dat1.find('ebay.com') != -1:
                ebay = dat1
            elif dat1.find('amazon.com') != -1:
                amazon = dat1
            else:
                errostr = '输入数据错误:%s'%(dat1)
                print(errostr.decode())
        else:
            try:
                tmp = int(dat1)
                ebay = dat1
            except Exception as e:
                amazon = dat1

        if dat2[:4] == 'http':
            if dat2.find('ebay.com') != -1:
                ebay = dat2
            elif dat2.find('amazon.com') != -1:
                amazon = dat2
            else:
                errostr = '输入数据错误:%s'%(dat2)
                print(errostr.decode())
        else:
            try:
                tmp = int(dat2)
                ebay = dat2
            except Exception as e:
                amazon = dat2
        return ebay,amazon

    def getTowObjData(self,pebay,pamazon,isFirst = False):
        ebayurl = ''
        amazurl = ''

        #173240166353
        #B079NP3NMH
        ebay,amazon = self.getRelUrl(pebay, pamazon)

        if ebay == '' or amazon == '':
            return

        if ebay[:4] == 'http':
            ebayurl = ebay
        else:
            ebayurl = 'https://www.ebay.com/itm/%s'%(ebay)
        if amazon[:4] == 'http':
            amazurl = amazon
        else:
            amazurl = 'https://www.amazon.com/dp/%s'%(amazon)

        objname = hashlib.sha256(ebayurl+amazurl).hexdigest()
        duboleobj = {}
        duboleobj['key'] = objname 
        duboleobj['ebay'] = self.getMsgWithURL_eBay(ebayurl)
        duboleobj['amazon'] = self.getMsgWithURL_Amazon(amazurl)
        if isFirst:
            duboleobj['time'] = int(time.time())
        return duboleobj

    def getOneData(self,preq):
        e,a = self.getRelUrl(preq, 'empty')
        outdat = None
        if e != '':
            eurl = ''
            if e[:4] == 'http':
                eurl = e
            else:
                eurl = 'https://www.ebay.com/itm/%s'%(e)
            outdat = self.getMsgWithURL_eBay(eurl)
        if a != '':
            aurl = ''
            if a[:4] == 'http':
                aurl = e
            else:
                aurl = 'https://www.amazon.com/dp/%s'%(a)
            outdat = self.getMsgWithURL_Amazon(aurl)
        return outdat

    def addNewDobuleURL(self,eurl,aurl):
        dictmp = self.getTowObjData(eurl, aurl,isFirst = True)
        value = json.dumps(dictmp)
        self.db.inset(dictmp['key'], value)

    def updateDictData(self):
        self.initTool()

    def updatePer2Hour(self):
        self.updateDictData()
        ptime = int(time.time())
        for k in self.dubDic.keys():
            etime = self.dubDic[k]['ebay']['time']
            atime = self.dubDic[k]['amazon']['time']
            if ptime - etime >= self.upTime or ptime - atime >= self.upTime:  #两小时更新一次
                eurl = self.dubDic[k]['ebay']['url']
                aurl = self.dubDic[k]['ebay']['url']
                dtmp = self.getTowObjData(eurl,aurl)
                dtmp['time'] = self.dubDic[k]['time']
                dtmp['key'] = k
                jstr = json.dumps(dtmp)
                self.db.update(k,jstr)
            dt = random.randint(1,5)
            time.sleep(dt)   #延时一个随军机秒数，再更新下一个

def main():
    tool = BS4HTMLTool()
    tool.getMsgWithURL_eBay('https://www.ebay.com/itm/173240166353')
    tool.getMsgWithURL_Amazon('https://www.amazon.com/dp/B079NP3NMH')

def test():
    tool = BS4HTMLTool()
    dobj = tool.getTowObjData('https://www.ebay.com/itm/173240166353', 'https://www.amazon.com/dp/B079NP3NMH')
    

#测试
if __name__ == '__main__':
    # main()
    test()





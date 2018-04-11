#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#https服务器
import os
import ssl
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import cgi
import time
import posixpath
import urllib
import sys
import shutil
import mimetypes
import json
import base64
import hashlib

import datetime


import zlib

# import Cookie

import BS4HTMLTool


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

nowPth = os.path.split(os.getcwd())[1]
curdir = '.'

import socket
hostname = socket.gethostname()
selfip = socket.gethostbyname(hostname)

setLastIP = selfip

reload(sys)  
sys.setdefaultencoding('utf8')  

print 'selfIP:',selfip
print 'setLastIP:',setLastIP


configdic = {}

users = {}

usercookies = []

bs4Requesttool = BS4HTMLTool.BS4HTMLTool()

def updateUser():
    global configdic
    global users
    global usercookies
    f = open('./config.txt','r')
    jstr = f.read()
    f.close()
    configdic = json.loads(jstr)
    users = configdic['user']
    usercookies = []
    for k in users:
        tmpcookie = hashlib.md5(k + users[k]).hexdigest()
        usercookies.append(tmpcookie)

updateUser()

#获取cookie过期时间
def getNewCookieExpTime():
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)  
    return expiration

import urllib

def addTowURL(ebayurl,amazonurl):
    # {'amazonitem': 'amazon', 'ebayitem': 'ebayurl'}
    global bs4Requesttool
    print(ebayurl)
    ebayurl = urllib.unquote(ebayurl).decode('utf-8', 'replace').encode('gbk', 'replace')
    print(ebayurl)
    print(amazonurl)
    amazonurl = urllib.unquote(amazonurl).decode('utf-8', 'replace').encode('gbk', 'replace')
    print(amazonurl)
    isOK = bs4Requesttool.addNewDobuleURL(ebayurl, amazonurl)
    return isOK



def createTableTR(dat,isAdditem = False):
    
    amazonurl = dat['amazon']['url']
    aimg = dat['amazon']['imgname']
    anametmp = dat['amazon']['name']
    anametmp = anametmp[12:97]
    aname = '''<a href="%s" target="view_window">%s</a>'''%(amazonurl,anametmp)
    
    aprice = dat['amazon']['price']

    ebayurl = dat['ebay']['url']
    eimg = dat['ebay']['imgname']
    enametmp = dat['ebay']['name'][:85]

    ename = '''<a href="%s" target="view_window">%s</a>'''%(ebayurl,enametmp)

    eprice = dat['ebay']['price']
    
    

    createtime = dat['time']
    createtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(createtime))
    createtimes = createtime.split(' ')
    createtime = '%s<p>%s</p>'%(createtimes[0],createtimes[1])
    uptime = dat['ebay']['time']
    uptime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(uptime))
    uptimes = uptime.split(' ')
    uptime = '%s<p>%s</p>'%(uptimes[0],uptimes[1])

    trid = dat['key']
    # print(aprice)
    # print(eprice)
    try:
        aprice = float(aprice[1:])
    except Exception as e:
        aprice = 0.0
    try:
        eprice = float(eprice[1:])
    except Exception as e:
        eprice = 0.0
    
    pricecolor = ''
    sp = 0
    if aprice == 0:
        sp = aprice-eprice
        subprice = '亚马逊价格错误'
    elif eprice == 0:
        subprice = 'ebay价格错误'
    else:
        sp = aprice-eprice
        subprice = '$%.2f'%(sp)
        if sp < 0:
            pricecolor = 'color:#19cb1d;'
        elif sp > 0:
            pricecolor = 'color:#e92020;'

    tabdel = ''''''
    if isAdditem:
        #增加册除行from
        tabdel = '''
            <td valign="middle" align="center" width="40" height="40" style='text-align:center;'>
                <form id="formdel" name="formdel" action="./del" method='get' target="del_frame">
                    <input type="hidden" name="tid" value="%s" />
                    <input type="submit" value="删除"/>
                </form>
            </td>
        '''%(trid)
  #   tmphtml = '''
  #   <tr>
  #       <td>
  #           <div class="boximg">
  #               <img src="./../img/%s.jpg" width="80" height="80" border="0" style=" vertical-align:middle;"/>
  #           </div>
  #       </td>
  #       <td width="300" height="80" align="center" valign="middle" style="word-break: break-all; word-wrap: break-all; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; display: block; font-size: 14px;">
  #               %s
  #       </td>
  #       <td valign="middle" align="center" width="120" height="80" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 16px; color:#b81820;font-weight:bold;">
  #           %s
  #       </td>
  #       <td valign="middle" align="center" width="120" height="80" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 16px; color:#b81820;font-weight:bold;">
  #           %s
  #       </td>
  #       <td valign="middle" width="300" height="80" style="word-break:break-all;word-wrap:break-all;text-overflow:ellipsis;overflow-y:hidden;overflow-x:hidden;display:block;font-size: 14px;">
  #           %s
  #       </td>
  #       <td>
  #           <div class="boximg">
  #               <img src="./../img/%s.jpg" width="80" height="80" border="0" style=" vertical-align:middle;"/>
  #           </div>
  #       </td>
  #       <td valign="middle" align="center" width="120" height="80" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 12px;">%s</td>

  #       <td valign="middle" align="center" width="120" height="80" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 12px;">%s</td>

  #       <td valign="middle" align="center" width="120" height="80" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 16px;font-weight:bold;%s">%s</td>
  # </tr>\n
  #   '''%(aimg,aname,aprice,eprice,ename,eimg,str(createtime),str(uptime),pricecolor,str(subprice))
    tmphtml = '''
    <tr>
        <td>
            <div class="boximg">
                <img src="./../img/%s.jpg" width="40" height="40" border="0" style=" vertical-align:middle;"/>
            </div>
        </td>
        <td width="300" height="40" align="center" valign="middle" style="word-break: break-all; word-wrap: break-all; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; display: block; font-size: 14px;">
                %s
        </td>
        <td valign="middle" align="center" width="120" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 16px; color:#b81820;font-weight:bold;">
            %s
        </td>
        <td valign="middle" align="center" width="120" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 16px; color:#b81820;font-weight:bold;">
            %s
        </td>
        <td valign="middle" width="300" height="40" style="word-break:break-all;word-wrap:break-all;text-overflow:ellipsis;overflow-y:hidden;overflow-x:hidden;display:block;font-size: 14px;">
            %s
        </td>
        <td>
            <div class="boximg">
                <img src="./../img/%s.jpg" width="40" height="40" border="0" style=" vertical-align:middle;"/>
            </div>
        </td>
        <td valign="middle" align="center" width="120" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 12px;">%s</td>

        <td valign="middle" align="center" width="120" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 12px;">%s</td>

        <td valign="middle" align="center" width="120" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 16px;font-weight:bold;%s">%s</td>

        %s
  </tr>
    \n

    '''%(aimg,aname,aprice,eprice,ename,eimg,str(createtime),str(uptime),pricecolor,str(subprice),tabdel)
    return [sp,tmphtml]

listhtmppth = curdir + os.sep +'html' + os.sep + 'listframe.html'
laddhtmlth = curdir + os.sep +'html' + os.sep + 'laddframe.html'
#从数据生成一个html网页
def createListHtml(isAdditem = False):
    global bs4Requesttool
    datdic = bs4Requesttool.getAllDic()
    #duboleobj['key'] = objname
    #duboleobj['ebay'] = {'imgurl':imgurl,'imgname':imgSaveName,'name':title,'price':price,'time':int(time.time()),'market':'ebay','url':purl}
    #duboleobj['amazon'] = {'imgurl':imgurl,'imgname':imgSaveName,'name':title,'price':price,'time':int(time.time()),'market':'amazon','url':purl}
    #duboleobj['time'] = time
    f = None
    if isAdditem:
        f = open(laddhtmlth,'r')
    else:
        f = open(listhtmppth,'r')
    liststr = f.read()
    f.close()
    fpot = liststr.find('$1')
    epot = liststr.find('$2') + 2

    fhtml = liststr[:fpot]

    ehtml = liststr[epot:]

    outhtml = fhtml + '\n'

    outs = []
    for k in datdic.keys():

        outtmp = createTableTR(datdic[k],isAdditem)
        outs.append(outtmp)

    outs.sort(reverse = False)  #按差价从小到大排序

    for d in outs:
        outhtml += d[1]
    outhtml += ehtml

    return outhtml

class myHandler(BaseHTTPRequestHandler):
    
    global bs4Requesttool
    #刷新数据
    def addItems(self,itemsobj):
        print(itemsobj)
        print(type(itemsobj))
        if addTowURL(itemsobj['ebayitem'], itemsobj['amazonitem']):
            # fpth = curdir + os.sep + 'html' + os.sep + 'list.html'
            # self.sendHtml(fpth)
            # htmlstr = createListHtml()
            # self.sendHtmlStr(htmlstr)
            jobj = {'erro':0,'msg':'添加商品成功'}
            msg = json.dumps(jobj,ensure_ascii=False)
            self.sendTxtMsg(msg)
        else:
            self.sendTxtMsg('添加商品失败，请查看输入地址是否正确.')
    def removeItem(self,tid):
        bs4Requesttool.removeOneDataWithKey(tid)
        jobj = {'erro':0,'msg':'删除商品成功'}
        msg = json.dumps(jobj,ensure_ascii=False)
        self.sendTxtMsg(msg)
    def login(self,logindat):
        print(logindat)
        # self.sendMsg('login')
        # {'pwd': 'aaa', 'usename': 'aaa'}
        if logindat['usename'] in users and logindat['pwd'] == users[logindat['usename']]:
            fpth = curdir + os.sep + 'html' + os.sep + 'list.html'
            sessionstr = hashlib.md5(logindat['usename'] + logindat['pwd']).hexdigest()
            cookiestr = "sessionID=%s"%(sessionstr)
            self.sendHtml(fpth,cookiestr)
        else:
            outobj = {"erro":1001,"msg":"用户名不存在或密码错误"}
            jstr = json.dumps(outobj,ensure_ascii=False)
            fpth = curdir + os.sep + 'html' + os.sep + 'loginerro.html'
            self.sendHtml(fpth)
    def checkCookie(self,cookiestr):
        if cookiestr:
            updateUser()
            tmpss = cookiestr.split('=')[1]
            if tmpss in usercookies:
                return True
        return False
    def do_GET(self):  
    	print('clientIP-->',self.client_address[0])
        print('clienturl-->',self.path)
        cookiestr = self.headers.getheader('Cookie');
        print('clientcookie---->',cookiestr)
        if self.path=="/":  
            if self.checkCookie(cookiestr):
                self.path="/list.html"
            else:
                self.path="/index.html"  
        try:  
            #根据请求的文件扩展名，设置正确的mime类型  
            if self.path.endswith(".html"):  
                if self.checkCookie(cookiestr):
                    if self.path[-14:] == 'listframe.html':
                        htmlstr = createListHtml()
                        self.sendHtmlStr(htmlstr)
                    elif self.path[-14:] == 'laddframe.html':
                        htmlstr = createListHtml(isAdditem = True)
                        self.sendHtmlStr(htmlstr)
                    else:
                        fpth = curdir + os.sep + 'html' + os.sep + self.path
                        self.sendHtml(fpth)
                else:
                    fpth = curdir + os.sep + 'html' + os.sep + 'index.html'
                    self.sendHtml(fpth)
                return
            elif self.path[1:4] == 'img':
                fpth = curdir + self.path
                self.sendImage(fpth)
            elif self.path[1:6] == 'login':#客户端登录
                print('login--->',self.path)
                return 'login'
            elif self.path[1:8] == 'additem': #增加新商品
                print('additem---->',self.path)

                return 'additem'
            elif self.path[1:4] == 'del':
                if self.checkCookie(cookiestr):
                    print(self.path)
                    tidtmp = self.path.split('?')[1]
                    dats = tidtmp.split('=')
                    print(dats)
                    ktmp = dats[0]
                    tid = dats[1]
                    self.removeItem(tid)
                else:
                    jobj = {'erro':1,'msg':'用户未登陆'}
                    msg = json.dumps(jobj,ensure_ascii=False)
                    self.sendTxtMsg(msg)
                    return
            else:
                time.sleep(3)
                self.sendEmptyMsg()
            return  
        except IOError:  
            self.send_error(404,'File Not Found: %s' % self.path)  

    def sendHtmlStr(self,htmlstr):
        mimetype='text/html'  
        self.send_response(200)  
        self.send_header('Content-type',mimetype)  
        self.end_headers()
        self.wfile.write(htmlstr)  

    def sendImage(self,imgpth):
        f = open(imgpth, 'rb') 
        mimetype='image/*'  
        self.send_response(200)  
        self.send_header('Content-type',mimetype)  
        self.end_headers()
        self.wfile.write(f.read())  
        f.close()  
    
    def sendHtml(self,fpth,pcookie = None):
        f = open(fpth, 'rb') 
        mimetype='text/html'  
        self.send_response(200)  
        if pcookie:
            print(pcookie)
            self.send_header("Set-Cookie",pcookie)
        self.send_header('Content-type',mimetype)  
        self.end_headers()
        self.wfile.write(f.read())  
        f.close()  

    def decodePostData(self,strdata):
        tmps = strdata.split('&')
        out = {}
        for d in tmps:
            objtmp = d.split('=')
            out[objtmp[0]] = objtmp[1]
        return out

    def do_POST(self):

        reqtype = self.do_GET()
        # try:
        if True:
            length = self.headers.getheader('content-length');
            nbytes = int(length)
            data = self.rfile.read(nbytes)
            msgobj = self.decodePostData(data)
            if reqtype == 'login':  
                updateUser()
                self.login(msgobj)
            elif reqtype == 'additem':
                self.addItems(msgobj)
            elif self.path == "/index.html":
                return
            else:
                self.sendEmptyMsg()

        # except Exception as e:
            # self.send_error(404,'File Not Found: %s' % self.path)  
    def sendEmptyMsg(self):
        self.send_response(200)
        self.send_header("Content-type", 'text/json; encoding=utf-8')
        self.send_header("Content-Length", str(''))
        self.end_headers()
        self.wfile.write('')



    def sendTxtMsg(self,msg,isCompress = False):
        outstr = ''
        if isCompress:
            demsg = self._compress(msg)
            outstr = base64.b64encode(demsg)
        else:
            outstr = msg
        self.send_response(200)
        self.send_header("Content-type", 'text/json;charset=utf-8')
        self.send_header("Content-Length", str(len(outstr)))
        self.end_headers()
        self.wfile.write(outstr)

    #校验消息真实性
    def verifyMsg(self,reqdict):
        tokenver = []
        tokenver.append('tokenxxx')
        tokenver.append(reqdict['nonce'])
        tokenver.append(reqdict['timestamp'])
        tokenver.sort()
        tmpstr = tokenver[0] + tokenver[1] + tokenver[2]
        sha1str = hashlib.sha1(tmpstr).hexdigest()
        if sha1str == reqdict['signature']:
            return True
        else:
            return False

    def _compress(self,msg):
        dat = zlib.compress(msg, zlib.Z_BEST_COMPRESSION)
        # print('ziplen-co-->',len(msg),len(dat))
        return dat
    def _decompress(self,dat):
        msg = zlib.decompress(dat)
        # print('ziplen-de-->',len(dat),len(msg))
        return msg


    def do_HEAD(self):
        """Serve a HEAD request."""
        print('do_HEAD')
        f = self.send_head()
        if f:
            f.close()

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write('''<form action="" enctype="multipart/form-data" method="post">\n
                    <input name="file" type="file" />
                    <input value="upload" type="submit" />
                </form>''')
        f.write("<hr>\n<ul>\n")
        for name in list:
            if name.startswith('.'):
                continue
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def log_error(self, format, *args):
        """Log an error.

        Display error message in red color.
        """

        format = '\033[0;31m' + format + '\033[0m'
        self.log_message(format, *args)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


tmpIp = configdic['ip']
tmpPort = configdic['port']

serverAddr = (selfip,tmpPort)

if selfip[0:2] != '19':
    serverAddr = (tmpIp,tmpPort)

def runHttpServer(ptemp):

    server = ThreadedHTTPServer(serverAddr, myHandler)
    print('https server is running....')
    print('Starting server, use <Ctrl-C> to stop')
    print(serverAddr)
    
    # server.socket = ssl.wrap_socket (server.socket, certfile='./keys/server.pem', server_side=True)
    server.serve_forever()
def startServer():

    thr = threading.Thread(target=runHttpServer,args=(None,))
    thr.setDaemon(True)
    thr.start()


if __name__ == '__main__':
    # server = ThreadedHTTPServer(serverAddr, myHandler)
    # print 'https server is running....'
    # print 'Starting server, use <Ctrl-C> to stop'
    # server.socket = ssl.wrap_socket (server.socket, certfile='server.pem', server_side=True)
    # server.serve_forever()
    ptime = 60*60*2
    tool = BS4HTMLTool.BS4HTMLTool(ptime)
    delaytime = tool.upTime
    startServer()
    while True:
        print('update 2hour')
        tool.updatePer2Hour()
        print('update 2hour end')
        time.sleep(delaytime)


# # 生成rsa密钥
# $ openssl genrsa -des3 -out server.key 2048
# # 去除掉密钥文件保护密码
# $ openssl rsa -in server.key -out server.key
# # 生成ca对应的csr文件
# $ openssl req -new -key server.key -out server.csr
# # 自签名
# $ openssl x509 -req -days 2048 -in server.csr -signkey server.key -out server.crt
# $ cat server.crt server.key > server.pem

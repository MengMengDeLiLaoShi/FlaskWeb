import re
import urllib
import urllib.request
import urllib.parse
import http.cookiejar
import gzip


def ungzip(data):
    '''请求的url内容是经过压缩的，需要解压后才能decode'''
    try:
        data = gzip.decompress(data)
    except:
        print('解压失败')
    return  data

def getToken(data):
    '''获取csrf跨站请求伪造，网页通过每次访问时随机生成一个csrf在post时提交csrf来'''
    cer = re.compile('<meta name="csrf-token" content="(.*)"')
    Token = cer.findall(data)
    return Token[0]

def getOpener(head):
    '''使用opener管理cookie,相当于浏览器去访问'''
    cj = http.cookiejar.CookieJar()#创建CookieJar对象，在内存中管理cookie
    pro = urllib.request.HTTPCookieProcessor(cj)#生成HTTPCookieProcessor对象
    opener = urllib.request.build_opener(pro)#生成opener对象
    '''修改http报头'''
    header = []
    for key,value in head.items():
        elem = (key,value)
        header.append(elem)
    opener.addheaders = header
    return opener

header = {
'Host':'59.108.56.172',
'Connection':'keep-alive',#urllib源码中把connection写死成了close，ddinfourl这个类一旦启用长链接，可以读取到上次交互未读完的应答报文，为了防止此类情况，所以强制性将Connection写死成close
'Cache-Control':'max-age=0',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer':'http://59.108.56.172/redmine/login?back_url=http%3A%2F%2F59.108.56.172%2Fredmine%2F',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8'}

url = 'http://59.108.56.172/redmine/login?back_url=http%3A%2F%2F59.108.56.172%2Fredmine%2F'

opener = getOpener(header)
op = opener.open(url)
data = op.read()
data = ungzip(data)
Token = getToken(data.decode())
username = 'liujiang'
password = 'HISliujiang'
utf8 = '✓'
login = '登录 »'
back_url = 'http://59.108.56.172/redmine/'
postDict = {
'authenticity_token':Token,
'username':username,
'password':password,
'utf8':utf8,
'login':login,
'back_url':back_url
}

postData = urllib.parse.urlencode(postDict).encode()
op = opener.open(url,postData)
op = opener.open('http://59.108.56.172/redmine/projects/his_client/issues/new')
data = op.read()
data = ungzip(data)
print(data.decode())

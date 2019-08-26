##

DEBUG = True 
EXAMPLE_URL = 'https://huaban.com/boards/37528906/' #示例网址
# EXAMPLE_URL = 'https://huaban.com/boards/42010879/'
HTML_ENCODING = 'utf8'


img_host = { 
    "hbimg": "img.hb.aicdn.com",
    "hbfile": "hbfile.b0.upaiyun.com/img/apps" 
}
hbfile = {
     "hbfile": "hbfile.b0.upaiyun.com", 
     "hbimg2": "hbimg2.b0.upaiyun.com"
}


#import urllib,urllib2,sys,os,time,json
import sys,os,time,json
import re
from urllib.request import urlopen,urlretrieve

#Get Page source
def writeToFile(data,filename):
    f= open(filename,"w+")
    f.write(data)
    f.close

def getPage(url,encoding=None):
    res = urlopen(url) #open->res
    page = res.read()
    
    if not encoding == None:
        page = page.decode(encoding)

    if DEBUG:
        writeToFile(page,"dudehtml.html")

    return page

#根据pin获取图片地址
def getFileSrc(pin):
    #pin是json里面的pin
    bucket = pin['file']['bucket']
    key = pin['file']['key']
    base_url = img_host[bucket]
    return "http://{0}/{1}".format(base_url,key)


#根据pin获取图片扩展名,不带.
def getFileExt(pin):
    type = pin['file']['type']
    type = type[type.index('/')+1:] #去掉 image/jpeg 前面的

    type = type.lower()
    if type == 'jpeg' or type == 'pjpeg':
        return 'jpg'
    else :
        return type

#将data的所有pin添加到pins
def addToPins(data):
    for p in data['pins']:
        pin_id = p["pin_id"]
        pin_src = getFileSrc(p)
        pin_ext = getFileExt(p)

        pin = (pin_id,pin_src,pin_ext)
        global pins
        pins.append(pin)

#parse args to get target url
def getUrlArg():
    if DEBUG:  
        url = EXAMPLE_URL
    elif len(sys.argv) == 1:
        print(u"Please provide the board URL:(example{0})".format(EXAMPLE_URL))
        exit()
    else: 
        url = sys.argv[1]

    if not url.endswith('/'):
        url = url + '/'
    return url


def getBoardMeta(html):
    pinCount = int(re.search(r'收入([0-9]*)',html).group(1))
    boardName = re.search(r'class="board-name">(.*)</h1>',html).group(1)

    return pinCount,boardName

class Pin:
    id = 0
    src = 'none'

def main():
    url = getUrlArg()
    html = getPage(url,"utf8")
    
    pinCount, boardName = getBoardMeta(html)
     IMAGE_DIR

    pins = [] #(id,src,ext)


    #首页的pins
    addToPins(data)

    page_num = pinCount/100 +1 #555个要加载6次
    for i in range(1,page_num+1):
        max = pins.pop()[0] #取pins的最后一个的id,同时删除最后一个,后面还要添加它
        url = argUrl + '?max={0}&&limit=101'.format(max)
        data = decodeJson(url)
        addToPins(data)

    ########################################################################
    #pins里面包含数据,开始下载
    print(u"图片系列为 : {0}".format(title))
    print(u"共{0}张图片,画板作者为 : {1}".format(count,username))
    print('')
    #image文件夹
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    #子文件夹
    if not os.path.exists(IMAGE_DIR + "/" + title):
        os.mkdir(IMAGE_DIR + "/" + title) #以title新建文件夹

    index = 1 #第几张图片
    for p in pins:
        #p = (id,src,ext)
        num = "{0:0{1}}".format(index,len(str(count)))
        ext = p[2] #jpg
        src = p[1] #http://xxx
        path = u"{0}/{1}/{2}.{3}".format(IMAGE_DIR,title,num,ext)
        print(u"正在下载第{0}张 : {1}".format(num,src))     
        urlretrieve(src,path)
        index+=1

if __name__ == '__main__':
    main()

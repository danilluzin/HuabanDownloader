##

DEBUG = True
# DEBUG = False 

# EXAMPLE_URL = 'https://huaban.com/boards/37528906/' #hair
# EXAMPLE_URL = 'https://huaban.com/boards/48685125/' #mood
EXAMPLE_URL = 'https://huaban.com/boards/31714128/' #art
HTML_ENCODING = 'utf8'
IMAGE_DIR = 'huaban'


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
import requests
import re
from urllib.request import urlopen,urlretrieve

#Get Page source
def writeToFile(data,filename):
    f= open(filename,"w+")
    f.write(data)
    f.close

def getPage(url,encoding=HTML_ENCODING):
    res = urlopen(url) #open->res
    page = res.read()
    
    if not encoding == None:
        page = page.decode(encoding)

    if DEBUG:
        writeToFile(page,"dudehtml.html")

    return page

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
    pinID = 0
    src = 'none'
    def __init__(self,_pinID,_src):
        self.pinID = _pinID
        self.src = _src

FAILED_PINS = []

def extendPinList(html,pins):
    print("Collecting pin info...")
    pinPattern = r'<a href="/pins/([0-9]*)/" .*?<img src="//(.*?)" width'
    matchList = re.findall(pinPattern,html)
    for pinId, src in matchList:
        src = "http://" + src.replace("hbimg.huabanimg.com","img.hb.aicdn.com") 
        src = re.sub("_fw[0-9]*$","",src) #size toke removal
        pins.append(Pin(pinId,src))

    print("Got more "+str(len(matchList))+" pins")


def createFolders(boardName):
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    
    if not os.path.exists(IMAGE_DIR + "/" + boardName):
        os.mkdir(IMAGE_DIR + "/" + boardName)


def getImage (url, filename, pinID):
    if os.path.exists(filename):
        print("skipping [already downloaded]")
        return
    done = False
    attempts = 10
    while not done:
        try:
            request = requests.get(url, timeout=10, stream=True)
            with open(filename, 'wb') as fh:
                for chunk in request.iter_content(1024 * 1024):
                    fh.write(chunk)
                    attempts = 10
            done = True
        except Exception as _:
            print("Timeout: pin "+ str(pinID))
            attempts = attempts - 1
            if attempts==0 :
                print("FAILED pin " + str(pinID))
                FAILED_PINS.append((pinID,url))
                if os.path.exists(filename):
                    os.remove(filename)
                return;
       

def main():
    argURL = getUrlArg()
    html = getPage(argURL)
    
    pinCount, boardName = getBoardMeta(html)
    print("Board: "+boardName+ " | number: "+str(pinCount))

    pins = [] #(id,src,ext)
    extendPinList(html,pins)

    page_num = int(pinCount/100) + 1

    for _ in range(1, page_num+1):
        lastPin = pins[-1].pinID 
        url = argURL + '?max={0}&&limit=101'.format(lastPin)
        html = getPage(url)
        extendPinList(html,pins)

    print("Got info for " + str(len(pins)) + " pins")
    
    createFolders(boardName);
    
    print("Downloading images")
    index = 0
    for p in pins:
        index += 1
        path = "{0}/{1}/{2}.{3}".format(IMAGE_DIR,boardName,p.pinID,"jpg")
        print("pin: " + str(p.pinID)+"  | " +str(index) +"/" +str(pinCount)) 
        getImage(p.src, path,p.pinID)
        # urlretrieve(p.src,path)

    print("Done!")
    if(len(FAILED_PINS)>0):
        f= open(IMAGE_DIR+'/'+boardName+'/'+"failReport.txt","w+")
        for fail in FAILED_PINS:
            f.write(str(fail[0]) + " : " + fail[1])
        f.close


if __name__ == '__main__':
    main()

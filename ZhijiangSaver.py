from random import random
from sseclient import SSEClient
from pyquery import PyQuery as pq
import time,random
import zmail
import requests
import threading

global timeLimit
global timer
timeLimit = 0
timer = threading.Timer

requestsHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Connection": "keep-alive"
}

cookie = {
    'cookie': r''
}

user = ""
password = ""
theHost = ""

theServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                         pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)

theRequestConn = requests.session()


def getContent(oriDom: pq):
    oriDom("script").remove()
    oriDom("input").remove()
    oriDom("form").remove()
    return oriDom(".article")


def existMorePages(oriDom):
    if oriDom(".paginator").length > 0:
        return True


def getSearchList(domTrees: pq):
    tempTrees = domTrees(".paginator")
    tempTrees("span").remove()
    return [ele.attr("href") for ele in tempTrees(".paginator")("a").items()]


def provideContent(url):
    try:
        html = theRequestConn.get(
            url=url, headers=requestsHeaders, cookies=cookie).content
        dom = getContent(pq(html))
        if existMorePages(dom):
            theList = getSearchList(dom)
            print(theList)
            index = 0
            for ele in theList:
                if index == 3:
                    break
                print("现在获取第" + str(index+1) + "页的内容....")
                newHtml = theRequestConn.get(
                    url=ele, headers=requestsHeaders, cookies=cookie).content
                newDom = getContent(pq(newHtml))
                newDom.insert_after(dom(":last"))
                time.sleep(random.randint(3,9))
                index = index + 1
        return dom
    except Exception as e:
        print("["+getTime()+"]"+"error occur when trying getting all content")
        print(e)


def getNotification():
    url = "https://www.douban.com/notification/"
    try:
        html = theRequestConn.get(
            url=url, headers=requestsHeaders, cookies=cookie).content
        processNotification(html)
    except Exception as e:
        print("["+getTime()+"]"+"error occur when GetNotification")
        print(e)

def sendEmail(mailStruct):
    try:
        print(mailStruct)
        theServer.send_mail("ava@mail.otterdaily.cn",mailStruct)
        
    except Exception as e:
        print("["+getTime()+"]"+"error occur when send mail")
        print("["+getTime()+"]"+e)


def processNotification(content):
    allDom = pq(content)
    operDom = allDom(".item-req:first")
    if "@" in operDom.text():
        try:
            url = operDom('a:first').attr('href')
            print("Save for:"+url)
            dom: pq = provideContent(url)
            subject = "[" + url.split("/topic/")[1] + "]" + dom('h1:first').text() + " " + dom('h3:first')('span:first').text()
            mailStruct = {
                'subject': subject,
                'content_html': dom.html(),
            }
            sendEmail(mailStruct=mailStruct)
            print("["+getTime()+"]"+"Finish saving")
        except Exception as e:
            print("["+getTime()+"]"+"error occur when processNotification")
            print("["+getTime()+"]"+e)
    else:
        print("["+getTime()+"]"+"not a @")


def getTime():
    return time.asctime(time.localtime(time.time()))

def limitClean():
    global timeLimit
    global timer
    timeLimit = 0
    print("["+getTime()+"]" + "重置备份限制")
    timer = threading.Timer(60.0,limitClean)
    timer.start()


limitClean()
sendUrl = ""
messages = SSEClient(sendUrl)
for msg in messages:
    print("["+getTime()+"]"+"检测到新消息")
    if timeLimit > 10:
        print("["+getTime()+"]"+"由于次数限制，不作存档。")
        continue
    getNotification()

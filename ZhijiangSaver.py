from random import random
from sseclient import SSEClient
from pyquery import PyQuery as pq
import time,random
import zmail
import requests
import threading 


# @variable timeLimit 访问次数限制。
# @variable timer 计时器。
# @variable requestsHeader 请求头。目前是按照cookie进行登陆的，日后考虑更换为移动端api进行登陆。
# @variable cookie cookie
# @variable user 登陆邮箱的账号名
# @variable password 登陆邮箱的密码
# @variable theHost 邮箱服务器主机
# @instance theServer 连接邮箱实例
# @instance theRequestConn requests实例，用于发起GET请求获取通知内容与页面内容。

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
    'cookie': r'll="118172"; bid=4_9Vn3iZ1pw; __yadk_uid=Ikn5yiZvj0Fr3ZR2EQSX8ZC8G6YrnFRG; douban-fav-remind=1; gr_user_id=12375f91-6d72-42d9-97b0-83145fe1d3a9; viewed="3168129_1374009_26416562_25720141"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1663900342%2C%22https%3A%2F%2Fgithub.com%2FWendaoLee%2Fdoubansaver%22%5D; _pk_ses.100001.8cb4=*; ap_v=0,6.0; dbcl2="229488397:jnbdYmoHgX4"; ck=NYNZ; push_doumail_num=0; _pk_id.100001.8cb4=e308c8c595b70eaf.1653107776.128.1663900640.1663508262.; push_noty_num=27'
}

theRequestConn = requests.session()

# 去除网页不必要内容，返回内容主体
def getContent(oriDom: pq):
    oriDom("script").remove()
    oriDom("input").remove()
    oriDom("form").remove()
    return oriDom(".article")

# 判断帖子是否存在多个页面
def existMorePages(oriDom):
    if oriDom(".paginator").length > 0:
        return True

# 在存在多个页面时调用，用于获取其他页面的链接
def getSearchList(domTrees: pq):
    tempTrees = domTrees(".paginator")
    tempTrees("span").remove()
    return [ele.attr("href") for ele in tempTrees(".paginator")("a").items()]

# 获取帖子内容，返回对应操作的dom实例
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

# 接收到通知时调用，用于获取被艾特的帖子的链接信息
def getNotification():
    url = "https://www.douban.com/notification/"
    try:
        html = theRequestConn.get(
            url=url, headers=requestsHeaders, cookies=cookie).content
        with open("./log.html",'w+',encoding='utf-8') as f:
            f.write(str(html))
        processNotification(html)
    except Exception as e:
        print("["+getTime()+"]"+"error occur when GetNotification")
        print(e)

def sendEmail(mailStruct):
    try:
        print(mailStruct)
        # theServer.send_mail("ava@mail.otterdaily.cn",mailStruct)
        
    except Exception as e:
        print("["+getTime()+"]"+"error occur when send mail")
        print("["+getTime()+"]"+e)

# 处理通知，获取内容，并发送邮件
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

# 清空次数限制。这并不是一个好的写法，但我没想太多。
def limitClean():
    global timeLimit
    global timer
    timeLimit = 0
    print("["+getTime()+"]" + "重置备份限制")
    timer = threading.Timer(60.0,limitClean)
    timer.start()


if __name__ == "__main__":
    print("hello")
    getNotification()
# sendUrl = ""
# messages = SSEClient(sendUrl)
# for msg in messages:
#     print("["+getTime()+"]"+"检测到新消息")
#     if timeLimit > 10:
#         print("["+getTime()+"]"+"由于次数限制，不作存档。")
#         continue
#     # 其实我应该把它写成链式的，现在确实代码挺丑陋的
#     getNotification()

from flask import Flask
from flask import render_template
from flask import Markup
import zmail
import time
import threading

global theNameList, theSortedIdList,theDateList
global theMailSum
global theUpdateTime

theNameList = []
theSortedIdList = []
theDateList = []
theUpdateTime = time.asctime(time.localtime(time.time()))
user = ""
password = ""
theHost = ""

mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                   pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)
theMailSum = mailServer.stat()[0]
del mailServer

def updateLatest():
    global theMailSum
    global theNameList
    global theSortedIdList
    global theDateList
    global theUpdateTime

    try:
        mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                   pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)
        print("周期更新 in " + time.asctime(time.localtime(time.time())))

        theMailSum = mailServer.stat()[0]
        tempNameList = []
        tempSortedList = []
        tempDateList = []

        temp = mailServer.get_mails(start_index=theMailSum-10,end_index=theMailSum)
        for ele in temp:
            tempNameList.append(ele['subject'])
            tempSortedList.append(ele['id'])
            tempDateList.append(ele['date'])
        theNameList = tempNameList
        theSortedIdList = tempSortedList
        theDateList = tempDateList
        theUpdateTime = time.asctime(time.localtime(time.time()))
    except Exception as e:
        print("Error occurs in " + time.asctime(time.localtime(time.time())))
        print(e)
    finally:
        threading.Timer(120.0,updateLatest).start()

updateLatest()

app = Flask(__name__)


@app.route('/')
def index():
    global theNameList
    global theSortedIdList
    global theUpdateTime
    print(theNameList)
    theHtml = "<ul>"
    item = ""
    # <li>" + str(theDateList[index]) + "--" +
    for index in range(0,len(theNameList)):
        item = "<li><a href='./mail/"+ str(theSortedIdList[index]) + "'>"+ theNameList[index] +"</a>" + "</li>"
        theHtml = theHtml + item
    theHtml = theHtml + "</ul>"
    return render_template("index.html",list=Markup(theHtml),updateTime=theUpdateTime)

@app.route('/mail/<mailkey>')
def getMail(mailkey):
    try:
        mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                   pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)
        content = mailServer.get_mail(mailkey)
        return render_template("mail.html",content=Markup(str(content['content_html']).replace('\\n','')),header=content['subject'],date=content['date'],id=content['id'])
    except Exception as e:
        print("Error occurs in " + time.asctime(time.localtime(time.time())))
        print(e)
        

@app.route('/search/<searchkey>')
def test(searchkey):
    try:
        mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)
        thelist = mailServer.get_mails(subject=searchkey)
        theHtml = "<ul>"
        item = ""
        for ele in thelist:
            item = "<li>" + str(ele['date']) + "--" + "<a href='../mail/" + str(ele['id']) +"'>" + ele['subject'] + "</a></li>"
            theHtml = theHtml + item
        theHtml = theHtml + "</ul>"
        return render_template("searchList.html",searchkey=searchkey,thehtml=Markup(theHtml))
    except Exception as e:
        print("Error occurs in " + time.asctime(time.localtime(time.time())))
        print(e)
 

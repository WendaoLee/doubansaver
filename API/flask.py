from flask import Flask,jsonify
from threading import Timer
import zmail

# @variable INFOQUEUE 常用的信息池
# [{
#   "id":xx,
#   "title":"xxx"
#   "topicNo":"xxx"
#   "author":"xxx"
# }]
INFOQUEUE = []

class KEY:
    ID = "id"
    TITLE = "title"
    TOPICNO = "topicNo"
    AUTHOR = "author"

def fuc_getINFOQUEUE():
    global INFOQUEUE
    INFOQUEUE.clear()
    theMailSum = mailServer.stat()[0]
    mails = mailServer.get_mails(start_index=theMailSum-10,end_index=theMailSum)
    for ele in mails:
        ob = fuc_getObject()
        ob[KEY.ID] = ele["id"]
        temp = ele["subject"].split("/]")[1]
        ob[KEY.TOPICNO] = ele["subject"].split("/]")[0].split("[")[1]
        ob[KEY.TITLE] = temp.split("来自:")[0]
        ob[KEY.AUTHOR] = temp.split("来自:")[1]
        INFOQUEUE.append(ob)
    INFOQUEUE.reverse()


def fuc_getObject():
    return {
        "id":0,
        "title":"null",
        "topicNo":"null",
        "author":"null"
    }

def fuc_freshInstance():
    global mailServer
    if mailServer is None:
        mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                   pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)
    else:
        del mailServer
        mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                   pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)
    
def fuc_timeCycle():
    fuc_freshInstance()
    Timer(60*60,fuc_timeCycle).start()

def state_timeCycle():
    fuc_getINFOQUEUE()
    Timer(60*1,state_timeCycle).start()

user = ""
password = ""
theHost = ""

mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                   pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)

app = Flask(__name__)
state_timeCycle()
fuc_timeCycle()

@app.route('/api/getLatest',methods=['GET'])
def getLatest():
    global INFOQUEUE
    return jsonify(str(INFOQUEUE))

@app.route('/api/getmailInfo/<mailkey>',methods=['GET'])
def getmailByKey(mailkey):
    global mailServer
    content = mailServer.get_mail(mailkey)
    return jsonify(str(content['content_html']).replace('\\n',''))

@app.route('/api/search/<searchkey>',methods=['GET'])
def searchKey(searchkey):
    global mailServer
    thelist = mailServer.get_mails(subject=searchkey)
    resultsList = []
    for ele in thelist:
        ob = {
            "id":"null",
            "title":"null"
        }
        ob[KEY.ID] = ele['id']
        ob[KEY.TITLE] = ele['subject']
        resultsList.append(ob)
    resultsList.reverse()
    return jsonify(str(resultsList))
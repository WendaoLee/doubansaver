from flask import Flask, jsonify
import threading
import time
import zmail

# @variable INFOQUEUE 常用的信息池
# [{
#   "id":xx,
#   "title":"xxx"
#   "topicNo":"xxx"
#   "author":"xxx"
# }]
global info_queue
info_queue = []

user = ""
password = ""
theHost = ""

class KEY:
    ID = "id"
    TITLE = "title"
    TOPICNO = "topicNo"
    AUTHOR = "author"


# @todo:添加异常字符串的解决方案（也许可以用正则表达式？）
def fuc_updateLatest():
    global info_queue
    info_queue.clear()

    try:
        mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                                  pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)
        print("更新Latest池 in " + time.asctime(time.localtime(time.time())))

        theMailSum = mailServer.stat()[0]
        mails = mailServer.get_mails(
            start_index=theMailSum-10, end_index=theMailSum
        )

        for ele in mails:
            ob = fuc_getObject()
            ob[KEY.ID] = ele["id"]
            subject = ele["subject"].split("/]")
            # 遇到邮件非常规解析，出现如“[271194173/?start=0#4754211748]”等字样的临时丑陋解决方案
            if len(subject) != 2:
                first_crpt = subject[0].split("/")[0]
                ob[KEY.TOPICNO] = first_crpt.split("[")[1]
                second_crpt = subject[0].split("]")[1]
                ob[KEY.TITLE] = second_crpt.split("来自:")[0]
                ob[KEY.AUTHOR] = second_crpt.split("来自:")[1]
                continue
            temp = ele["subject"].split("/]")[1]
            ob[KEY.TOPICNO] = ele["subject"].split("/]")[0].split("[")[1]
            ob[KEY.TITLE] = temp.split("来自:")[0]
            ob[KEY.AUTHOR] = temp.split("来自:")[1]
            info_queue.append(ob)
        info_queue.reverse()
        print("正常完成更新")
        
    except Exception as e:
        print("Error occurs in " + time.asctime(time.localtime(time.time())))
        print(e)
        info_queue.reverse()
        print("此时，queue为:")
        print(info_queue)
    finally:
        threading.Timer(120.0, fuc_updateLatest).start()


def fuc_getObject():
    return {
        "id": 0,
        "title": "null",
        "topicNo": "null",
        "author": "null"
    }


app = Flask(__name__)

fuc_updateLatest()

@app.route('/api/getLatest', methods=['GET'])
def getLatest():
    global info_queue
    return jsonify(str(info_queue))


@app.route('/api/getmailInfo/<mailkey>', methods=['GET'])
def getmailByKey(mailkey):
    mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                              pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)
    content = mailServer.get_mail(mailkey)
    return jsonify(str(content['content_html']).replace('\\n', ''))


@app.route('/api/search/<searchkey>', methods=['GET'])
def searchKey(searchkey):
    mailServer = zmail.server(user, password, smtp_host=theHost, smtp_port=25, pop_host=theHost,
                              pop_port=110, pop_ssl=False, pop_tls=False, smtp_ssl=False, smtp_tls=False)
    thelist = mailServer.get_mails(subject=searchkey)
    resultsList = []
    for ele in thelist:
        ob = {
            "id": "null",
            "title": "null"
        }
        ob[KEY.ID] = ele['id']
        ob[KEY.TITLE] = ele['subject']
        resultsList.append(ob)
    resultsList.reverse()
    return jsonify(str(resultsList))

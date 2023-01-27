import time
from multiprocessing import Process,Pipe

import requests.exceptions

from .theSSEClient import DoubanSSEListener
from .noticeParser import NotificationGetter
from .mobile import createNewTask
from .utils import getSSEPipeMsg, SSE_isValueNeedChange,getCookieDict

from orm.database import DataBaseConnector
from orm.utils import normalCheck

from multiprocessing.connection import PipeConnection


def SSE_InvokeSubProcess(sub_pipe: PipeConnection, sseurl: str, cookie: str, db: DataBaseConnector):
    """调起SSE子进程

    规定SSE子进程与主进程之间的管道通信格式为：
        Main -> SSE:
            {
                "signal":"end"||"continue", //指示是否继续该进程
                "sseurl":"{url}"||"null", //是否要更新sseurl，若需要，则传入url
                "cookie":"{cookie_str}"||"null", //是否要更新cookie
                “db”:DataBaseConnector||"null" //是否更新数据库链接
            }
        SSE -> Main:
            {
                "process": "SSE_SubProcess", //进程名
                "type": type, //消息类型
                "time": time.asctime(), //发生时间
                "msg": msg //消息
            }

    由于SSE监听循环的存在，通常情况下主进程不会主动传递消息。@Notice 这可能是一个引发问题的点，因为我们使用了Pipe进行通信。可能会因为主进程传递了无用的信息而造成在WaitForCall环节的无效更新，使进程依然无法正常工作

    内部定义了两个函数:
    :Involed-Function
        listener_loop:SSE监听循环。会在发生错误时结束循环。
        SSE_WaitForCall:当进程发生错误时调用，它会一直等待，直到主进程传递信号过来，而后根据信号决定是否终止或调整进程参数后重新调用listner_loop
    """

    def listener_loop(listener):
        """SSE监听循环。在确认SSE连接无误后会调用该函数启动监听"""
        for msg in listener:
            try:
                print(
                    '\u001b[36m [INFO] \u001b[0m Receive message,getting data......'
                )
                sub_pipe.send(
                    getSSEPipeMsg('Get Notification')
                )
                tasklist = NotificationGetter(cookie=cookie).get_notification()
                dataList = createNewTask(tasklist)
                normalCheck(db, dataList)
                sub_pipe.send(
                    getSSEPipeMsg('Finish')
                )
            except Exception as e:
                sub_pipe.send(
                    getSSEPipeMsg(type="Error", msg=e)
                )
                return 0

    def SSE_WaitForCall(the_pipe: PipeConnection):
        """当SSE进程出现问题时，调用它等待主进程回复，根据主进程信号决定之后的行为"""
        keepWaiting = True
        while keepWaiting:
            time.sleep(5)
            if the_pipe.poll():
                res_msg = the_pipe.recv()
                the_pipe.send(
                    getSSEPipeMsg(msg="Getting the context:\n {context}".format(str(res_msg)))
                )

                if res_msg['signal'] == 'end':
                    return False
                if SSE_isValueNeedChange('sseurl', res_msg):
                    nonlocal sseurl
                    sseurl = res_msg['sseurl']
                if SSE_isValueNeedChange('cookie', res_msg):
                    nonlocal cookie
                    cookie = res_msg['cookie']
                if SSE_isValueNeedChange('db', res_msg):
                    nonlocal db
                    db = res_msg['db']
                return True

    client = DoubanSSEListener(sseurl=sseurl)
    cookie = getCookieDict(cookie)
    try:
        listener = client.getListener()
        listener_loop(listener)
    except requests.exceptions.HTTPError as e:
        sub_pipe.send(getSSEPipeMsg(msg=e, type="Error"))
    except Exception as e:
        sub_pipe.send(
            getSSEPipeMsg(msg=e, type="Error")
        )
    finally:
        # 等待主进程回答，若等到回答会重新调用listener_loo[重启任务，反之则完成进程的所有任务，自动结束。
        if SSE_WaitForCall(the_pipe=sub_pipe):
            client = DoubanSSEListener(sseurl=sseurl)
            listener_loop(client.getListener())

if __name__ == "__main__":
    SSE_MainProcessPipe,SSE_SubProcessPipe = Pipe()
    p = Process(target=SSE_InvokeSubProcess,args=(
        SSE_SubProcessPipe,
        "https://push.douban.com:4397/sse?channel=notification:user:229488397&auth=229488397_1666261882:c69664d89862d90090e0c1d99f781075bb5f12f5",
        getCookieDict('ll="118172"; bid=4_9Vn3iZ1pw; __yadk_uid=Ikn5yiZvj0Fr3ZR2EQSX8ZC8G6YrnFRG; douban-fav-remind=1; gr_user_id=12375f91-6d72-42d9-97b0-83145fe1d3a9; viewed="3168129_1374009_26416562_25720141"; push_doumail_num=0; dbcl2="229488397:itFnTnfr6kI"; ck=d2dJ; push_noty_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1666253688%2C%22https%3A%2F%2Fgithub.com%2FWendaoLee%2Fdoubansaver%22%5D; _pk_ses.100001.8cb4=*; ap_v=0,6.0; _pk_id.100001.8cb4=e308c8c595b70eaf.1653107776.140.1666253692.1666243234.'),
        DataBaseConnector()
    ))
    p.start()
    for ele,value in SSE_MainProcessPipe.recv().items():
        print(value)
    print(1)
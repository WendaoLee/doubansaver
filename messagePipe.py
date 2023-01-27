from dataGetter.ProcessInvoker import SSE_InvokeSubProcess
from dataGetter.utils import destructSSEPipeMsg
from multiprocessing import Process,Pipe
from orm.database import DataBaseConnector


def start_SSE_subprocess(sseurl:str,cookie:str,db:DataBaseConnector):
    SSE_MainProcessPipe, SSE_SubProcessPipe = Pipe()
    p = Process(target=SSE_InvokeSubProcess, args=(
        SSE_SubProcessPipe,
        sseurl,
        cookie,
        db
    ))
    p.start()
    return SSE_MainProcessPipe


class MessagePipe(object):
    def quit(self):
        exit(1)

    commandDef = {
        "exit":quit
    }

    def __init__(self,out_buff):
        self.out_buff = out_buff

    def recive(self,command,value):
        self.commandDef[command]



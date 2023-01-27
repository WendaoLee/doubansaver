from .TerminalLogger import LOGGER

db_path = ""
sse_url = ""
cookie = ""


def set_global(dic:dict):
    global db_path,sse_url,cookie
    db_path = dic['database']
    sse_url = dic['sseurl']
    cookie = dic['cookie']
    LOGGER.DEBUG('global variable is \n'+
                 'db_path:'+db_path +
                 "\nsse_url:" + sse_url +
                 "\ncookie:" + cookie)

def change_db_path(path):
    global db_path
    db_path = path
    LOGGER.DEBUG('Change db_path to:' + db_path)

def change_sse_url(url):
    global sse_url
    sse_url = url
    LOGGER.DEBUG('Change sse_url to:' + sse_url)

def change_cookie(new_cookie):
    global cookie
    cookie = new_cookie
    LOGGER.DEBUG('Change cookie to:' + cookie)
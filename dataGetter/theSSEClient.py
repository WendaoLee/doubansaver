from sseclient import SSEClient

class DoubanSSEListener(object):
    def __init__(self, sseurl: str):
        self.url = sseurl

    def getListener(self):
        return SSEClient(self.url)

    def updateUrl(self,sseurl:str):
        self.url = sseurl
        return self


if __name__ =='__main__':
    ins = DoubanSSEListener(sseurl='https://push.douban.com:4397/sse?channel=notification:user:229488397&auth=229488397_1666242282:ff4601476dccb7d3a2b930184cc24246988d3485')
    a = ins.getListener()
    if any(a):
        print(a)


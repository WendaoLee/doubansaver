from pyquery import PyQuery as pq
from dataGetter.utils import getCookieDict, mapToTid, mapToUnique

import requests


class NotificationGetter(object):
    theRequestConn = None

    cookie = {
        'cookie': r''
    }
    requestsHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Connection": "keep-alive"
    }

    def __init__(self, cookie):
        self.url = "https://www.douban.com/notification/"
        self.cookie = cookie
        self.theRequestConn = requests.session()

    def get_notification(self):
        try:
            html = self.theRequestConn.get(
                url=self.url, headers=self.requestsHeaders, cookies=self.cookie).content
            ins = pq(str(html))('.notification-list')('.item-req')
            link_list = []
            ins.map(lambda ele, val: link_list.append(pq(val)('a').attr('href')))
            return mapToUnique(
                mapToTid(link_list)
            )
        except Exception as e:
            print("error occur when GetNotification")
            print(e)


if __name__ == "__main__":
    # with open('sample.html', encoding='utf-8', mode='r') as f:
    #     str = f.read()
    #
    # ins = pq(str)('.notification-list')('.item-req')
    # a = []
    # re = ins.map(lambda ele, val: a.append(pq(val)('a').attr('href')))
    # print(1)
    c = r'll="118172"; bid=4_9Vn3iZ1pw; __yadk_uid=Ikn5yiZvj0Fr3ZR2EQSX8ZC8G6YrnFRG; douban-fav-remind=1; gr_user_id=12375f91-6d72-42d9-97b0-83145fe1d3a9; viewed="3168129_1374009_26416562_25720141"; push_doumail_num=0; dbcl2="229488397:itFnTnfr6kI"; ck=d2dJ; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1666090032%2C%22https%3A%2F%2Fgithub.com%2FWendaoLee%2Fdoubansaver%22%5D; _pk_id.100001.8cb4=e308c8c595b70eaf.1653107776.136.1666090032.1666064497.; _pk_ses.100001.8cb4=*; ap_v=0,6.0; push_noty_num=0'
    # instance = NotificationGetter(
    #     utils.cookiejar_from_dict
    # )
    # instance.get_notification()
    a = []
    r = getCookieDict(c)

    # thelist = ['https://www.douban.com/group/topic/276942770/?start=0#4876980014', 'https://www.douban.com/group/topic/276706988/?start=0', 'https://www.douban.com/group/topic/276871935/?start=0', 'https://www.douban.com/group/topic/276871935/?start=0#4875664296', 'https://www.douban.com/group/topic/276871935/?start=0', 'https://www.douban.com/group/topic/276871935/', 'https://www.douban.com/group/topic/276871935/?start=0#4875557709', 'https://www.douban.com/group/topic/276871935/?start=0', 'https://www.douban.com/group/topic/276871935/?start=0', 'https://www.douban.com/group/topic/276871935/?start=0', 'https://www.douban.com/group/topic/276871935/?start=0', 'https://www.douban.com/group/65539/', 'https://www.douban.com/group/topic/276423355/?start=0', 'https://www.douban.com/group/topic/276423355/?start=0', 'https://www.douban.com/group/topic/273565435/?start=0#4873775910', 'https://www.douban.com/group/topic/273565435/?start=0#4873718267', 'https://www.douban.com/group/topic/276706988/?start=0#4872298236', 'https://www.douban.com/group/topic/276706988/?start=0#4872221197', 'https://www.douban.com/group/topic/276706988/?start=0#4871977799', 'https://www.douban.com/group/topic/276706988/?start=0#4872053599', 'https://www.douban.com/group/topic/276706988/?start=0', 'https://www.douban.com/group/topic/276706988/', 'https://www.douban.com/group/topic/276423730/?start=0', 'https://www.douban.com/group/topic/276423730/?start=0', 'https://www.douban.com/group/topic/276670463/?start=0#4871204960', 'https://www.douban.com/group/topic/276675253/?start=0#4871308951', 'https://www.douban.com/group/topic/276675253/?start=0#4871308892', 'https://www.douban.com/group/topic/276675253/?start=0#4871303802', 'https://www.douban.com/group/734219/', 'https://www.douban.com/group/topic/276345154/?start=300#4869581958', 'https://www.douban.com/group/topic/276540783/?start=0#4868928786', 'https://www.douban.com/group/topic/276345154/?start=300#4868840980', 'https://www.douban.com/group/topic/276345154/?start=300#4868838908', 'https://www.douban.com/group/topic/276345154/?start=300#4868674637', 'https://www.douban.com/group/topic/276537824/?start=0#4868576692', 'https://www.douban.com/group/topic/275953272/?start=0#4868332429', 'https://www.douban.com/group/topic/275953272/?start=0#4868151334']
    # a = mapToUnique(
    #     mapToTid(thelist)
    # )
    # print(a)
    # print(r)
    # # for ele in c.split(';'):
    # #     ele = ele.lstrip()
    # #     index = ele.find('=')
    # #     a.append(ele)
    # # map(lambda ele:)
    instance = NotificationGetter(
        cookie=r
    )
    aa = instance.get_notification()
    print(aa)

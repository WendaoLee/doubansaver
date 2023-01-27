"""
  Author:WendaoLee https://github.com/WendaoLee
"""

import requests
import json

class NotificationGetter():
    """To get notification from douban

    Member:
        url:Where notification can be get.
        header:request's header.
        cookie:Douban's cookie.
        config_path:Where config file in local disk.This can be write with hardcode.
    """
    url = ''
    header = ''
    cookie = ''
    config_path = ''

    def __init__(self,url:str,header:str,cookie:str):
        self.url = url
        self.header = header
        self.cookie = cookie
        self.connection = requests.session()


    def update_context(self,**kwargs):
        """Update the member of class.
        """
        for ele in kwargs:
            if ele in ["url","header","cookie"]:
                self[ele] = kwargs[ele]

    def update_context_from_config(self):
        """Update the member of class from the config
        """ 
        with open('./config.json','r',encoding='utf-8') as f:
            txt = f.read()
        json_struct = json.loads(txt)
        for ele in json_struct:
            if ele in ["url","header","cookie","config_path"]:
                self[ele] = json_struct[ele]
        return 0


if __name__ == "__main__":
    hand = NotificationGetter()

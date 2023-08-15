# -*- coding:utf-8 -*-
import time

import requests
import json
from util.logger import log


"""
    IP工具类
"""


class IpUtils:
    
    def __init__(self, key):
        self.key = key

    # 提取IP
    def get(self, num=1):
        # KeepAlive=1440 
        url = "https://proxy.qg.net/allocate?Key={}&Num={}&KeepAlive=1440".format(self.key, num)
        response = requests.get(url, timeout=30)
        data = json.loads(response.text)
        ips = list()
        if data.get("Code") == 0:
            for ip_dict in data.get("Data"):
                ips.append("{}:{}".format(ip_dict.get("IP"), ip_dict.get("port")))
            log.info("IP提取成功: {}".format(ips))

        return ips

    # 释放IP
    def release(self, proxy_list):
        ip_list = list()
        for proxy in proxy_list:
            ip_list.append(proxy.split(":")[0])

        url = "https://proxy.qg.net/release?Key={}&IP={}".format(self.key, ",".join(ip_list))
        response = requests.get(url, timeout=30)
        log.info("释放IP:{} {}".format(proxy_list, response.text))

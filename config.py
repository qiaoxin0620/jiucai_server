# -*- coding:utf-8 -*-
import configparser
import sys
import os
import re

auth_key = "775CF852"
auth_pwd = "B58539CE11DE"
tunnel = "tunnel6.qg.net:17739"  # 隧道

RabbitMqHost = "120.42.248.249"
RabbitMqPort = 5762
RabbitMqUser = "admin"
RabbitMqPass = "admin"

host = 'localhost'
port = 3306
user = 'root'
password = '123456'
database = 'jiucai'
RPA_TASK_HOST = "http://222.77.96.23:85/api/task/callback"
ProxyServer = "https://exclusive.proxy.qg.net/replace?key=D0A30620&num=1&keep_alive={}&area=350500&isp=&format=json&seq=&distinct=true"

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    # if __name__ == '__main__':
    base_path = os.path.dirname(os.path.abspath(__file__))
    # else:
    #     import __main__
    #     base_path = os.path.dirname(os.path.abspath(__main__.__file__)) if hasattr(__main__, '__file__') else None


DOMAIN_ZHAOPIN = "http://www.feikua.net"   # 飞跨 http://www.feikua.net/ 测试站 http://222.77.96.23:1001
DOMAIN_GEEK = "http://www.feikua.net"
DOMAIN_QG = "https://www.qg.net"

Phones = [
    # "17628312668",
    "19905950692", # 张晓莉
    "19905950697", # 洪新洲
    "19905950130", # 蔡艺婉 163 qg.net2015
    "19905950691", # 杨雪莲
    "all"]
BossDPDetailThreadNum = 5
BossLoginSleepTime = 30 * 60
BossLoginCrawlTimes = 650
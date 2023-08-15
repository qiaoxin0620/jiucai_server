#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import datetime
import os
import sys
from config import base_path

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    if __name__ == '__main__':
        base_path = os.path.dirname(os.path.abspath(__file__))
    else:
        import __main__
        base_path = os.path.dirname(os.path.abspath(__main__.__file__)) if hasattr(__main__, '__file__') else None


log_file = os.path.join(base_path, 'log', "{}.log".format(datetime.datetime.now().strftime('%Y%m%d')))
if not os.path.exists(os.path.join(base_path, 'log')):
    os.makedirs(os.path.join(base_path, 'log'))


class Log:
    def __init__(self):

        self.logger = logging.getLogger()

        self.logger.setLevel(logging.INFO)

        # 创建一个handle写入文件
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 创建一个handle输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义输出的格式
        formatter = logging.Formatter(self.fmt)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 添加到handle
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @property
    def fmt(self):
        return '%(levelname)s\t%(asctime)s\t[%(filename)s:%(lineno)d]\t%(message)s'


log = Log().logger

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/5/9
# @Author : Joker
# @Version : Python 3.7
# @Software: PyCharm
import os
import time
import logging
from frame.config import framePath, logOptions


class Logger:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = '%(asctime)s-%(levelname)s: %(message)s'
        self.formatter = logging.Formatter(formatter)
        self.formatter.default_time_format = "%H:%M:%S"

        self.log_name = self._log_name()

    @staticmethod
    def _log_name():
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        time_report_path = os.path.join(framePath.Report_Path, f"report_{day}")
        if not os.path.exists(time_report_path):
            os.makedirs(time_report_path)
        log_name = os.path.join(time_report_path, f"{day}.log")
        return log_name

    def create_log_handler(self):
        # 控制台日志输出
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logOptions.Stream_Loglevel)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)
        # 文件日志输出
        file_handler = logging.FileHandler(self.log_name, encoding="utf8")
        file_handler.setLevel(logOptions.File_Loglevel)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
        return self.logger


log = Logger().create_log_handler()


if __name__ == '__main__':
    log.info('test')
    log.error('error')

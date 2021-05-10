# -*- coding:utf-8 -*-
# @Time : 2021/5/10
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com

"""项目运行初始创建必要的文件夹"""
import os
import time
from frame.config import framePath

__all__ = ['TIME_REPORT_PATH', 'SCREENSHOT_PATH']


def init_path():
    day = time.strftime('%Y%m%d', time.localtime(time.time()))
    # 每次运行时存放结果的文件夹
    time_report_path = os.path.join(framePath.Report_Path, f"report_{day}")
    if not os.path.exists(time_report_path):
        os.makedirs(time_report_path)

    # 截图存在的文件夹
    screenshot_path = os.path.join(time_report_path, "screenshots")
    if not os.path.exists(screenshot_path):
        os.makedirs(screenshot_path)

    return time_report_path, screenshot_path


TIME_REPORT_PATH, SCREENSHOT_PATH = init_path()


if __name__ == '__main__':
    print(TIME_REPORT_PATH, SCREENSHOT_PATH)

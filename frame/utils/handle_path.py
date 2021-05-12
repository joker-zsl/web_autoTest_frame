# -*- coding:utf-8 -*-
# @Time : 2021/5/10
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com
import os
import time
import importlib
from frame.config import BASE_PATH, framePath

__all__ = ['TIME_REPORT_PATH', 'SCREENSHOT_PATH', 'load_module']


def load_module(package):
    """加载模块"""
    for path, dirs, files in os.walk(package):
        for file in files:
            if file.endswith('page.py'):
                file_path = os.path.join(path, file)[:-3]
                module_path = package_module_path(file_path)
                importlib.import_module(module_path)


def package_module_path(file_path):
    """包装导入模块所用的路径"""
    rel_path = file_path.replace(BASE_PATH, '')
    if '/' in rel_path:
        dir_list = [_ for _ in rel_path.split('/') if _]
    else:
        dir_list = [_ for _ in rel_path.split('\\') if _]
    module_path = '.'.join(dir_list)
    return module_path


def init_path():
    """创建报告和截图存放的文件夹"""
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
    pass


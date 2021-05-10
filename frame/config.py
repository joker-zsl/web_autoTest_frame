# -*- coding:utf-8 -*-
# @Time : 2021/5/8
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com

import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))


class FrameSetting:
    Browser_Type = 'chrome'  # chrome/chrome_mobile/firefox/ie/edge/phantomjs
    Wait_Time = 30  # 隐式等待设定的超时时间
    Timeout = 30  # 显式等待设定的超时时间
    Poll_Frequency = 0.2  # 显式等待设定的轮询时间
    Delay_Time = 1  # 截图的延迟时间(太快可能页面没渲染截不到想要的结果)
    Report_Keep_Counts = 10  # 测试报告保存份数


class BrowserOptions:
    """浏览器配置"""
    Download_Path = None
    Maximize_Window = True  # 窗口最大化
    Windows_Size = False  # 模拟移动端时一定要设置此项
    Windows_Width = 600
    Windows_Height = 900
    PIXEL_RATIO = 3.0
    Headless_Mode = False


class FramePath:
    """各文件(夹)路径"""
    Report_Path = os.path.join(BASE_PATH, "reports")  # 报告存放路径
    if not os.path.exists(Report_Path):
        os.makedirs(Report_Path)
    Driver_Path = os.path.join(BASE_PATH, "drivers")  # 浏览器驱动存放路径
    if not os.path.exists(Driver_Path):
        os.makedirs(Driver_Path)


class LogOptions:
    Stream_Loglevel = 'INFO'
    File_Loglevel = 'INFO'


class DriverPath:
    """驱动地址"""
    CHROME_DRIVER_PATH = os.path.join(FramePath.Driver_Path, "chromedriver89.0.4389.23.exe")
    FIREFOX_DRIVER_PATH = None
    IE_DRIVER_PATH = None
    EDGE_DRIVER_PATH = None
    PHANTOMJS_DRIVER_PATH = None


frameSetting = FrameSetting()
framePath = FramePath()
logOptions = LogOptions()
browserOptions = BrowserOptions()
driverPath = DriverPath()


if __name__ == '__main__':
    print(BASE_PATH)

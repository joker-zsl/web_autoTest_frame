# -*- coding:utf-8 -*-
# @Time : 2021/5/8
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com

from selenium import webdriver
from frame.config import ChromeOption


def chrome_options():
    """配置chrome浏览器"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')  # 使用这个属性规避谷歌浏览器的未知BUG
    options.add_experimental_option('w3c', False)  # 关闭谷歌浏览器的W3C检查

    if ChromeOption.Windows_Size:
        options.add_argument(ChromeOption.Windows_Size)
    else:
        options.add_argument('--start-maximized')  # 最大化窗口运行

    if ChromeOption.Headless_Mode:
        options.add_argument('--headless')

    if ChromeOption.Download_Path:
        prefs = {'download.default_directory': ChromeOption.Download_Path}
        options.add_experimental_option('prefs', prefs)
    return options


def chrome_mobile_options():
    """配置chrome浏览器模拟移动端配置"""
    options = chrome_options()
    User_Agent = r'--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 ' \
                 r'(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
    options.add_argument(User_Agent)
    mobile_emulation = {
        'deviceMetrics': {
            'width': ChromeOption.Windows_Width,
            'height': ChromeOption.Windows_Height,
            'pixelRatio': ChromeOption.PIXEL_RATIO
        }
    }
    options.add_experimental_option('mobileEmulation', mobile_emulation)
    return options


def IE_options():
    """配置IE浏览器"""
    options = webdriver.IeOptions()
    options.set_capability(options.IGNORE_ZOOM_LEVEL, True)
    options.set_capability(options.FORCE_CREATE_PROCESS_API, True)
    options.set_capability(options.SWITCHES, '-private')
    options.set_capability(options.NATIVE_EVENTS, False)
    return options


def firefox_options():
    """配置firefox浏览器"""
    pass


class Browser:
    def __init__(self, browser_type='chrome'):
        self.type = browser_type.lower()
        support_type_list = ['chrome', 'firefox', 'ie']
        if self.type in support_type_list:
            pass

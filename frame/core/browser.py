# -*- coding:utf-8 -*-
# @Time : 2021/5/8
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com

from selenium import webdriver
from frame.config import browserOptions, driverPath, frameSetting
from frame.core.errors import BrowserTypeError
from frame.utils.handle_log import log
from frame.core.decorators import singleton


def chrome_options():
    """配置chrome浏览器"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')  # 使用这个属性规避谷歌浏览器的未知BUG
    options.add_experimental_option('w3c', False)  # 关闭谷歌浏览器的W3C检查

    if browserOptions.Headless_Mode:
        options.add_argument('--headless')

    if browserOptions.Download_Path:
        prefs = {'download.default_directory': browserOptions.Download_Path}
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
            'width': browserOptions.Windows_Width,
            'height': browserOptions.Windows_Height,
            'pixelRatio': browserOptions.PIXEL_RATIO
        }
    }
    options.add_experimental_option('mobileEmulation', mobile_emulation)
    return options


def ie_options():
    """配置IE浏览器"""
    options = webdriver.IeOptions()
    options.set_capability(options.IGNORE_ZOOM_LEVEL, True)
    options.set_capability(options.FORCE_CREATE_PROCESS_API, True)
    options.set_capability(options.SWITCHES, '-private')
    options.set_capability(options.NATIVE_EVENTS, False)
    return options


def firefox_options():
    """配置firefox浏览器"""
    profile = webdriver.FirefoxProfile()
    if browserOptions.Download_Path:
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showhenStarting", False)
        profile.set_preference("browser.download.dir", browserOptions.Download_Path)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # 下载文件类型
    return profile


@singleton
class Browser:
    """
    灵活创建不同类型的浏览器
    """
    def __init__(self, browser_type='chrome'):
        self.type = browser_type.lower()
        support_type_list = ['chrome', 'chrome_mobile', 'firefox', 'ie', 'edge', 'phantomjs']
        if self.type not in support_type_list:
            log.error(f'while create browser not support this browser type: {self.type}')
            raise BrowserTypeError(f'not support this browser type: {self.type}')

        self.driver = self.create_driver()

    def _browser(self):
        browser = {
            'chrome': webdriver.Chrome,
            'chrome_mobile': webdriver.Chrome,
            'firefox': webdriver.Firefox,
            'ie': webdriver.Ie,
            'edge': webdriver.Edge,
            'phantomjs': webdriver.PhantomJS
        }
        return browser.get(self.type)

    def _executable_path(self):
        path = {
            'chrome': driverPath.CHROME_DRIVER_PATH,
            'chrome_mobile': driverPath.CHROME_DRIVER_PATH,
            'firefox': driverPath.FIREFOX_DRIVER_PATH,
            'ie': driverPath.IE_DRIVER_PATH,
            'edge': driverPath.EDGE_DRIVER_PATH,
            'phantomjs': driverPath.PHANTOMJS_DRIVER_PATH
        }
        return path.get(self.type)

    def _options(self):
        options = {
            'chrome': chrome_options(),
            'chrome_mobile': chrome_mobile_options(),
            'firefox': firefox_options(),
            'ie': ie_options()
        }
        return options.get(self.type)

    def create_driver(self):
        browser = self._browser()
        path = self._executable_path()
        options = self._options()
        if options:
            if self.type == 'firefox':
                driver = browser(executable_path=path, firefox_profile=options)
            else:
                driver = browser(executable_path=path, options=options)
        else:
            driver = browser(executable_path=path)

        driver.implicitly_wait(frameSetting.Wait_Time)

        if browserOptions.Windows_Size:
            driver.set_window_size(browserOptions.Windows_Width, browserOptions.Windows_Height)
        if browserOptions.Maximize_Window:
            driver.maximize_window()

        log.info(f'open browser: {self.type}')
        return driver


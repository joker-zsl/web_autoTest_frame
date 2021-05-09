#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/5/9
# @Author : Joker
# @Version : Python 3.7
# @Software: PyCharm
import os
import time
from PIL import Image, ImageDraw
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from frame.config import frameSetting, framePath
from frame.core.browser import Browser
from frame.core.errors import ParamsLoseError
from frame.utils.handle_log import log


class BrowserAction:
    """浏览器操作"""
    def __init__(self):
        self.driver = Browser(browser_type=frameSetting.Browser_Type).driver

    def get(self, url):
        """打开网页"""
        if not url.startswith('http') and not url.startswith('https'):
            url = f'http://{url}'
        self.driver.get(url)
        log.info(f'open page: {url}')
        return self

    def close(self):
        """关闭网页"""
        self.driver.close()
        log.info(f'close page: {self.current_url}')

    def refresh(self):
        """刷新网页"""
        self.driver.refresh()
        log.info(f'refresh page: {self.current_url}')

    def forward(self):
        """前进下一网页"""
        self.driver.forward()
        log.info(f'forward to the page: {self.current_url}')

    def back(self):
        """前进下一网页"""
        self.driver.back()
        log.info(f'back to the page: {self.current_url}')

    def switch_to_window(self, window_sign=None):
        """
        切换窗口
        :param window_sign: 要切换到的窗口的特征标志，可以是url或title中独有的部分字符串，窗口大于2个时必传
        """
        handles = self.window_handles
        if len(handles) == 1:
            log.warn('just on window, need not switch')
        elif len(handles) == 2:
            current_window_index = handles.index(self.current_window_handle)
            other_window_handle = handles[1 - current_window_index]
            self.driver.switch_to.window(other_window_handle)
            log.info(f'page switch to: {self.current_url}')
        else:
            if window_sign:
                for handle in handles:
                    self.driver.switch_to.window(handle)
                    if window_sign in self.current_url or window_sign in self.title:
                        log.info(f'page switch to: {self.current_url}')
                        break
            else:
                log.error('while switch_to_window lose necessary params: window_sign')
                raise ParamsLoseError('lose necessary params: window_sign')

    def quit(self):
        """关闭浏览器"""
        self.driver.quit()
        log.info('quit browser')

    @property
    def title(self):
        """当前页面的title"""
        title = self.driver.title
        log.info(f'get current page title: {title}')
        return title

    @property
    def current_url(self):
        """当前页面的URL"""
        current_url = self.driver.current_url
        log.info(f'get current page url: {current_url}')
        return current_url

    @property
    def window_handles(self):
        """全部窗口句柄"""
        handles = self.driver.window_handles
        log.info(f'get window handles: {handles}')
        return handles

    @property
    def current_window_handle(self):
        """当前窗口句柄"""
        handle = self.driver.current_window_handle
        log.info(f'get current window handle: {handle}')
        return handle


class PageAction:
    """页面元素操作"""
    def __init__(self):
        self.driver = Browser(browser_type=frameSetting.Browser_Type).driver
        self.screenshot_path = self._screenshot_path()

    def find_element(self, locator):
        """查找元素"""
        try:
            element = WebDriverWait(self.driver, frameSetting.Timeout, frameSetting.Poll_Frequency).until(
                ec.visibility_of_element_located(locator))
        except Exception as e:
            log.error(f'can not find element: {locator}')
            raise e
        else:
            log.info(f'find element: {locator}')
            return element

    def find_elements(self, locator):
        """查找多个元素"""
        try:
            elements = WebDriverWait(self.driver, frameSetting.Timeout, frameSetting.Poll_Frequency).until(
                ec.presence_of_all_elements_located(locator))
        except Exception as e:
            log.error(f'can not find elements: {locator}')
            raise e
        else:
            log.info(f'find elements: {locator}')
            return elements

    def click(self, locator):
        """点击元素"""
        try:
            element = WebDriverWait(self.driver, frameSetting.Timeout, frameSetting.Poll_Frequency).until(
                ec.element_to_be_clickable(locator))
            element.click()
        except Exception as e:
            log.error(f'can not click element: {locator}')
            raise e
        else:
            log.info(f'click element: {locator}')

    def send_keys(self, locator, msg):
        """输入"""
        element = self.find_element(locator)
        try:
            element.clear()
            element.send_keys(str(msg))
        except Exception as e:
            log.error(f'element: {locator} can not send msg: {msg}')
            raise e
        else:
            log.info(f'element: {locator} send msg: {msg}')

    def move_to_element(self, locator):
        """鼠标在元素上悬停"""
        action = ActionChains(self.driver)
        action.reset_actions()
        element = self.find_element(locator)
        try:
            action.move_to_element(element).perform()
        except Exception as e:
            log.error(f'can not move to element: {locator}')
            raise e
        else:
            log.info(f'move to element: {locator}')

    def switch_to_frame(self, frame_reference):
        """
        切换iframe
        :param frame_reference: iframe的name/id/index/<class 'WebElement'>
        """
        try:
            self.driver.switch_to.frame(frame_reference)
        except Exception as e:
            log.error('can not switch to new frame')
            raise e
        else:
            log.info('switch to new frame')

    def switch_to_parent_frame(self):
        """切换到父iframe"""
        try:
            self.driver.switch_to.parent_frame()
        except Exception as e:
            log.error('can not switch to parent frame')
            raise e
        else:
            log.info('switch to parent frame')

    def switch_to_default_content(self):
        """切换到主文档"""
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            log.error('can not switch to default content')
            raise e
        else:
            log.info('switch to default content')

    @staticmethod
    def _screenshot_path():
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        time_report_path = os.path.join(framePath.Report_Path, f"report_{day}")
        if not os.path.exists(time_report_path):
            os.makedirs(time_report_path)
        screenshot_path = os.path.join(time_report_path, "screenshots")
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        return screenshot_path

    def screenshot(self, locator=None):
        """截图"""
        time.sleep(frameSetting.Delay_Time)
        tm = str(float('%.2f' % time.time()))
        screenshot_name = os.path.join(self.screenshot_path, f"{tm}.png")
        self.driver.save_screenshot(screenshot_name)
        log.info(f'screenshot save: {screenshot_name}')
        # 标记元素
        # 谷歌浏览器模拟移动端时无法标记元素,暂时限定只有谷歌浏览器标记
        if locator and frameSetting.Browser_Type == 'chrome':
            element = self.find_element(locator)
            roll_left = self.driver.execute_script('return document.documentElement.scrollLeft;')
            roll_height = self.driver.execute_script('return document.documentElement.scrollTop;')
            top_x = element.location['x']
            top_y = element.location['y']
            abs_x = top_x - roll_left
            abs_y = top_y - roll_height
            bottom_x = abs_x + element.size['width']
            bottom_y = abs_y + element.size['height']
            with Image.open(screenshot_name) as img:
                draw = ImageDraw.Draw(img)
                draw.rectangle([abs_x, abs_y, bottom_x, bottom_y], outline='RED', width=3)
                img.save(screenshot_name)


class Driver(PageAction, BrowserAction):
    pass




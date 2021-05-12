# -*- coding:utf-8 -*-
# @Time : 2021/5/11
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com
import os
import time
from frame.core.driver import Driver
from frame.core.errors import ParamsError, ExecuteStepError
from frame.core.decorators import keyword
from frame.config import BASE_PATH
from frame.utils.handle_log import log
from frame.utils.handle_path import load_module


class Step:
    """用例行数据组成的对象"""
    def __init__(self, params: dict):
        self.step = params.get('step')
        self.action = params.get('action')
        self.params = params.get('params', '')
        self.explain = params.get('explain')

    def __str__(self):
        s = {
            "step": self.step,
            "action": self.action,
            "params": self.params,
            "explain": self.explain
        }
        return str(s)


class ProcessHandle:
    def __init__(self):
        self.driver = None
        self.images_info = []
        self.keywords = self.load_keyword()

    def set_driver(self):
        self.driver = Driver()

    @staticmethod
    def load_keyword():
        """加载关键字"""
        package = os.path.join(BASE_PATH, 'pages')
        load_module(package)
        from frame.core.decorators import keyword_pool
        return keyword_pool

    def execute_step(self, step_dict):
        """
        执行用例里的每步操作
        :param step_dict: 用例的行数据 dict {"step":1,"action":"login","params":"admin,admin","explain":"登录"}
        :return:
        """
        if not self.driver:
            self.set_driver()

        step = Step(step_dict)  # 整理下数据方便后面使用
        if step.action:
            return self.dispatch(step)
        else:
            log.error(f'not find action in this step: {step}')
            raise ParamsError('this step lose action')

    def dispatch(self, step):
        try:
            func = self.keywords[step.action]
            param_count = func.__code__.co_argcount  # 判断关键字函数形参个数
            if param_count == 1:
                result = self.keywords[step.action](self)
            else:
                params = str(step.params).split(',')
                result = self.keywords[step.action](self, *params)
        except Exception as e:
            self.step_error_teardown(step, e)
        else:
            self.step_teardown(step)
            return result

    @staticmethod
    def step_error_teardown(step, e):
        """处理步骤执行后发生的错误"""
        log.error(f'dispatch step: {step} happen error: {e}')
        raise ExecuteStepError(e)

    def step_teardown(self, step):
        """步骤执行后的收尾工作"""
        # 在BasePage子类中复写此方法
        pass


class BasePage(ProcessHandle):

    def step_teardown(self, step):
        """步骤执行后的收尾工作"""
        self.screenshot_to_report(step=step)

    def screenshot_to_report(self, locator=None, step=None):
        """
        截图并包装成html模板 记录到属性中
        :param locator: 元素定位，如果传值，则截图时对此元素进行标记
        :param step: 步骤结束后调用会传此步骤的信息，如果在方法中自己使用，可以传说明信息，会在报告展示截图时一起展示
        :return:
        """
        img_path = self.driver.screenshot(locator)
        img_record_template = """
            <div><img src="%s" width=100%%;/></div>
            <div style='margin: 5px;  padding-right: 5px; width: 100%%; height: 34px; overflow: hidden;'>
                <span>%d.%s</span>
            </div>
        """
        img_info = img_record_template % (img_path, len(self.images_info) + 1, step)
        self.images_info.append(img_info)

    @keyword()
    def get(self, url):
        self.driver.get(url)

    @keyword()
    def close(self):
        self.driver.close()

    @keyword()
    def wait(self, wait_time):
        time.sleep(int(wait_time))

    @keyword()
    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    handle = ProcessHandle()
    print(handle.keywords)

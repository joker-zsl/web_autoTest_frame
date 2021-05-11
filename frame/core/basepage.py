# -*- coding:utf-8 -*-
# @Time : 2021/5/11
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com
from frame.core.driver import Driver
from frame.core.errors import ParamsError, ExecuteStepError
from frame.core.decorators import keyword
from frame.utils.handle_log import log


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
        self.driver = Driver()
        self.images_info = []

    def execute_step(self, step_dict):
        """
        执行用例里的每步操作
        :param step_dict: 用例的行数据 dict {"step":1,"action":"login","params":"admin,admin","explain":"登录"}
        :return:
        """
        step = Step(step_dict)  # 整理下数据方便后面使用
        if step.action:
            return self.dispatch(step)
        else:
            log.error(f'not find action in this step: {step}')
            raise ParamsError('this step lose action')

    def dispatch(self, step):
        try:
            func = keyword_pool[step.action]
            param_count = func.__code__.co_argcount  # 判断函数形参个数
            if param_count == 1:
                result = keyword_pool[step.action](self)
            else:
                params = step.params.split(',')
                result = keyword_pool[step.action](self, *params)
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
        self.screenshot_to_report(step)

    def screenshot_to_report(self, step):
        """截图并包装成html模板 记录到属性中"""
        img_path = self.driver.screenshot()
        img_record_template = """
            <div><img src="%s" width=100%%;/></div>
            <div style='margin: 5px;  padding-right: 5px; width: 100%%; height: 34px; overflow: hidden;'>
                <span>%d.%s</span>
            </div>
        """
        img_info = img_record_template % (img_path, len(self.images_info) + 1, step)
        self.images_info.append(img_info)


class BasePage(ProcessHandle):

    @keyword()
    def get(self, a):
        self.driver.get('http://baidu.com')
        print(a)

    def quit(self):
        pass


if __name__ == '__main__':
    from pages.test_page import *
    from frame.core.decorators import keyword_pool
    print(keyword_pool)
    step = {"step":1,"action":"get","params":"admin","explain":"登录"}
    handle = ProcessHandle()
    handle.execute_step(step)
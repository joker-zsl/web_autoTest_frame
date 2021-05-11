# -*- coding:utf-8 -*-
# @Time : 2021/5/11
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com
import os
import unittest
from frame.core.basepage import BasePage
from frame.config import BASE_PATH
from frame.utils.handle_excel import ReadExcel
from frame.utils.handle_log import log


class TestInfo:
    controlPanel_path = os.path.join(BASE_PATH, 'testcases', 'ControlPanel.xlsx')  # 控制面板路径
    controlPanel_sheet = 'test'  # 测试用例在控制面板中的sheet
    testcase_dir = os.path.join(BASE_PATH, 'testcases', 'cases')  # 存放测试用例的文件夹


class TestCase(unittest.TestCase, TestInfo):
    """组织测试用例的通用模板"""
    def setUp(self) -> None:
        self.case_image = []  # 保存截图信息
        case_path = os.path.join(self.testcase_dir, f'{self._testMethodName}.xlsx')
        self.flow_path = ReadExcel(case_path, 'flowPath').data().value  # 测试用例里的流程
        self.handler = BasePage()
        # self.handler.get('http://baidu.com')
        log.info('=========================START=========================')
        log.info(f'execute testcase: {self._testMethodName}')

    def test_case(self):
        for step in self.flow_path:
            self.handler.execute_step(step)
        self.case_image = self.handler.images_info

    def tearDown(self) -> None:
        self.handler.quit()
        log.info(f'end of execution testcase: {self._testMethodName}')
        log.info('========================= END =========================')


testcase_class = {

}

# -*- coding:utf-8 -*-
# @Time : 2021/5/11
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com

import unittest
from frame.core.testcase import testcase_class, TestCase
from frame.utils.handle_excel import ReadExcel


class TestSuite:
    def __init__(self, name):
        """
        :param name: 要执行的测试用例名，是testcase_class的一个key
        """
        self.suite = unittest.TestSuite()
        self.name = name

    def case_class(self):
        """测试用例所属测试类"""
        return testcase_class.get(self.name, TestCase)

    def case_datas(self):
        test_class = self.case_class()
        filename = test_class.controlPanel_path
        sheetname = test_class.controlPanel_sheet
        datas = ReadExcel(filename, sheetname).data().filter_by(execute='Yes')
        return datas

    def set_case_info(self):
        pass

    def load(self):
        pass

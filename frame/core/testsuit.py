# -*- coding:utf-8 -*-
# @Time : 2021/5/11
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com
import os
import unittest

from frame.core.errors import LoadCaseError
from frame.core.testcase import testcase_class, TestCase
from frame.utils.handle_excel import ReadExcel
from frame.utils.handle_log import log


class TestSuite:
    """组装测试套件"""
    def __init__(self, name):
        """
        :param name: 要执行的测试用例名，是testcase_class的一个key
        """
        self.name = name
        self.suite = unittest.TestSuite()
        self.test_class = self.case_class()

    def case_class(self):
        """测试用例所属测试类"""
        return testcase_class.get(self.name, TestCase)

    def case_datas(self):
        """全部测试用例数据"""
        filename = self.test_class.controlPanel_path
        sheetname = self.test_class.controlPanel_sheet
        datas = ReadExcel(filename, sheetname).data().filter_by(execute='Yes')
        return datas

    def set_case_info(self, case_class, case_name, description):
        """设置测试用例的所属类和用例描述 class_name, method_name, method_doc"""
        setattr(case_class, case_name, case_class.test_case)
        testcase = getattr(case_class, case_name)
        testcase.__doc__ = description
        self.suite.addTest(case_class(case_name))

    def load(self):
        """装载测试用例"""
        cls = self.test_class
        cases = self.case_datas()
        testcase_dir = cls.testcase_dir
        if cases:
            for case in cases:
                case_name = case['casename']
                description = case['description']
                case_file_path = os.path.join(testcase_dir, '%s.xlsx' % case_name)
                if os.path.exists(case_file_path):
                    self.set_case_info(cls, case_name, description)
                    log.info(f'success to add testcase: {case_name}')
                else:
                    log.warn(f'fail to add testcase: {case_name}')
            return self.suite
        else:
            log.error('not find execute case')
            raise LoadCaseError('no case can be load. Please check ControlPanel')

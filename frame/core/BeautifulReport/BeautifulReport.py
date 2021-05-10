import os
import re
import sys
import time
import json
import unittest
import traceback
from io import StringIO as StringIO
from frame.utils.handle_path import TIME_REPORT_PATH

__all__ = ['BeautifulReport']


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp
    
    def write(self, s):
        self.fp.write(s)
    
    def writelines(self, lines):
        self.fp.writelines(lines)
    
    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

resultData = {
    "testPass": 0,
    "testResult": [
    ],
    "testName": "",
    "testAll": 0,
    "testFail": 0,
    "beginTime": "",
    "totalTime": "",
    "testSkip": 0
}

beautiful_report_dir_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
template_path = os.path.join(beautiful_report_dir_path, 'template.html')  # 模板文件路径


class MakeResultJson:
    """组装测试结果行数据"""
    def __init__(self, datas: tuple):
        """
        :param datas: testcase所携带的信息,用于报告table > th 的数据展示
        """
        self.datas = datas
        self.result_schema = {}
    
    def __setitem__(self, key, value):
        self[key] = value
    
    def __repr__(self) -> str:
        """
        :return: 返回一个构造完成的表单th数据
        """
        keys = ('className', 'methodName', 'description', 'spendTime', 'status', 'log', 'image')
        for key, data in zip(keys, self.datas):
            self.result_schema.setdefault(key, data)
        return json.dumps(self.result_schema)


class ReportTestResult(unittest.TestResult):
    def __init__(self, suite, stream=sys.stdout):
        """ pass """
        super(ReportTestResult, self).__init__()
        self.begin_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.start_time = 0
        self.stream = stream
        self.end_time = 0
        self.failure_count = 0
        self.error_count = 0
        self.success_count = 0
        self.skipped = []
        self.suite = suite
        self.status = ''
        self.default_report_name = '自动化测试报告'
        self.sys_stdout = None
        self.sys_stderr = None
        self.outputBuffer = None
        self.resultData = resultData
        self.result_list = []
        self.case_log = []
        self._mirrorOutput = False  # print(class_name, method_name, method_doc)
    
    @property
    def success_counter(self) -> int:
        """设置成功次数"""
        return self.success_count
    
    @success_counter.setter
    def success_counter(self, value) -> None:
        """
        success_counter函数的setter方法, 用于改变成功的case数量
        :param value: 当前传递进来的成功次数的int数值
        :return:
        """
        self.success_count = value
    
    def startTest(self, test) -> None:
        """
        测试用例运行前调用
        """
        unittest.TestResult.startTest(self, test)
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.sys_stdout = sys.stdout
        self.sys_stdout = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector
        self.start_time = time.time()
    
    def stopTest(self, test) -> None:
        """
        测试用例执行后调用
        """
        self.end_time = '{0:.3} s'.format((time.time() - self.start_time))
        self.result_list.append(self.get_all_result_info_tuple(test))
        self.complete_output()
    
    def complete_output(self):
        """
        断开输出重定向
        """
        if self.sys_stdout:
            sys.stdout = self.sys_stdout
            sys.stderr = self.sys_stdout
            self.sys_stdout = None
            self.sys_stdout = None
        return self.outputBuffer.getvalue()
    
    def stopTestRun(self, title=None) -> dict:
        """
            所有测试执行完成后, 执行该方法
        :param title:
        :return:
        """
        resultData['testPass'] = self.success_counter
        for item in self.result_list:
            item = json.loads(str(MakeResultJson(item)))
            resultData.get('testResult').append(item)
        resultData['testAll'] = len(self.result_list)
        resultData['testName'] = title if title else self.default_report_name
        resultData['testFail'] = self.failure_count
        resultData['beginTime'] = self.begin_time
        end_time = int(time.time())
        start_time = int(time.mktime(time.strptime(self.begin_time, '%Y-%m-%d %H:%M:%S')))
        resultData['totalTime'] = str(end_time - start_time) + 's'
        resultData['testError'] = self.error_count
        resultData['testSkip'] = self.skipped
        self.resultData = resultData
        return resultData

    @staticmethod
    def get_testcase_property(test) -> tuple:
        """
        返回一个test的class_name, method_name, method_doc属性
        :param test: testcase
        :return: (class_name, method_name, method_doc) -> tuple
        """
        class_name = test.__class__.__qualname__
        method_name = test.__dict__['_testMethodName']
        method_doc = test.__dict__['_testMethodDoc']
        return class_name, method_name, method_doc

    def get_all_result_info_tuple(self, test) -> tuple:
        """
        接受test相关信息, 并拼接成一个完成的tuple结构返回
        :param test: testcase
        :return: testcase要展示在页面的信息
        """
        try:
            case_images = test.case_image
        except AttributeError:
            case_images = []
        return tuple([*self.get_testcase_property(test), self.end_time, self.status, self.case_log, case_images])
    
    @staticmethod
    def error_or_failure_text(err) -> str:
        """
        获取sys.exc_info()的参数并返回字符串类型的数据, 去掉t6 error
        """
        return traceback.format_exception(*err)
    
    def addSuccess(self, test) -> None:
        logs = []
        output = self.complete_output()
        logs.append(output)
        sys.stderr.write('.')
        self.success_counter += 1
        self.status = '成功'
        self.case_log = output.split('\n')
        self._mirrorOutput = True
    
    def addError(self, test, err):
        logs = []
        output = self.complete_output()
        logs.append(output)
        logs.extend(self.error_or_failure_text(err))
        self.failure_count += 1
        self.add_test_type('失败', logs)
        sys.stderr.write('F')
        self._mirrorOutput = True
    
    def addFailure(self, test, err):
        logs = []
        output = self.complete_output()
        logs.append(output)
        logs.extend(self.error_or_failure_text(err))
        self.failure_count += 1
        self.add_test_type('失败', logs)
        sys.stderr.write('F')
        self._mirrorOutput = True
    
    def addSkip(self, test, reason) -> None:
        logs = [reason]
        self.complete_output()
        self.skipped += 1
        self.add_test_type('跳过', logs)
        sys.stderr.write('S')
        self._mirrorOutput = True
    
    def add_test_type(self, status: str, case_log: list) -> None:
        self.status = status
        self.case_log = case_log


class BeautifulReport(ReportTestResult):
    def __init__(self, suites):
        super(BeautifulReport, self).__init__(suites)
        self.suites = suites

    def run(self, description='自动化测试报告'):
        """
        生成测试报告
        """
        self.suites.run(result=self)
        self.stopTestRun(description)
        self.output_report()
    
    def output_report(self):
        """
        输出测试报告
        """
        day = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        filename = os.path.join(TIME_REPORT_PATH, f"report_{day}.html")
        with open(template_path, 'r', encoding='utf-8') as file:
            body = file.read()
        with open(filename, 'w') as write_file:
            item = re.search('\${resultData}', body).group()
            template = body.replace(item, json.dumps(self.resultData, ensure_ascii=False, indent=4))
            write_file.write(template)


# -*- coding:utf-8 -*-
# @Time : 2021/5/8
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com
from frame.core.testsuit import TestSuite
from frame.core.BeautifulReport import BeautifulReport


def main():
    suites = TestSuite('test').load()
    result = BeautifulReport(suites)
    result.run()


if __name__ == '__main__':
    main()

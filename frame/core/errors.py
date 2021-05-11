#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/5/8
# @Author : Joker
# @Version : Python 3.7
# @Software: PyCharm


class BrowserTypeError(Exception):
    """浏览器类型错误"""
    pass


class ParamsError(Exception):
    """参数错误"""
    pass


class ExecuteStepError(Exception):
    """执行用例步骤时发生错误"""
    pass

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/5/9
# @Author : Joker
# @Version : Python 3.7
# @Software: PyCharm
from functools import wraps


def singleton(cls):
    """单例模式"""
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton

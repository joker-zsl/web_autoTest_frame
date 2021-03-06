#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/5/9
# @Author : Joker
# @Version : Python 3.7
# @Software: PyCharm
from functools import wraps

from frame.core.errors import FunctionError
from frame.utils.handle_log import log

keyword_pool = {}


def keyword(kw=None):
    """添加关键字"""
    def add_keyword(func):
        key = kw if kw else func.__name__
        if func.__module__ != '__main__':
            if key in keyword_pool.keys():
                exist_func = keyword_pool[key]
                log.warn(f'exist same keyword: {key} {exist_func} {func}')
            keyword_pool[key] = func

    def inner(func):
        add_keyword(func)

        @wraps(func)
        def action(*args, **kwargs):
            return func(*args, **kwargs)
        return action
    return inner


def switch_to_frame(param=0):
    def inner(func):
        @wraps(func)
        def decorator(self, *args, **kwargs):
            if not hasattr(self, 'driver'):
                raise FunctionError(f'{type(self)} object has no attribute "driver"')
            self.driver.switch_to_frame(param)
            result = func(self, *args, **kwargs)
            self.driver.switch_to_parent_frame()
            return result
        return decorator
    return inner


def singleton(cls):
    """单例模式"""
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


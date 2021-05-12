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

        def action(*args, **kwargs):
            return func(*args, **kwargs)
        copy_properties(func, action)
        return action
    return inner


def switch_to_frame(param=0):
    def inner(func):
        def decorator(self, *args, **kwargs):
            if not hasattr(self, 'driver'):
                raise FunctionError(f'{type(self)} object has no attribute "driver"')
            self.driver.switch_to_frame(param)
            result = func(self, *args, **kwargs)
            self.driver.switch_to_parent_frame()
            return result
        copy_properties(func, decorator)
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


# def copy_properties(src):
#     """用于保持函数的属性"""
#     def wrapper(dst):
#         dst.__name__ = src.__name__
#         dst.__doc__ = src.__doc__
#         dst.__qualname__ = src.__qualname__
#         dst.__code__ = src.__code__
#         return dst
#     return wrapper

def copy_properties(src,dst):
    dst.__name__=src.__name__
    dst.__doc__=src.__doc__
    dst.__qualname__=src.__qualname__
    dst.__code__ = src.__code__

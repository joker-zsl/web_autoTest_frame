# -*- coding:utf-8 -*-
# @Time : 2021/5/11
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com

from frame.core.basepage import BasePage
from frame.core.decorators import keyword


class Test(BasePage):
    @keyword()
    def test(self):
        pass

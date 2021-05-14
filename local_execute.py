# -*- coding:utf-8 -*-
# @Time : 2021/5/12
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com
from frame.core.basepage import BasePage


def main(flow_path):
    handle = BasePage()
    print(handle.keywords)
    for step in flow_path:
        handle.execute_step(step)


if __name__ == '__main__':
    flow_path = [
        {'step': 1, 'action': 'get', 'params': 'https://ec2.51ykb.com/ecs-console/index.html#/login', 'explain': ''},
        {'step': 2, 'action': 'login', 'params': 'ceshi,999999', 'explain': None},
        {'step': 3, 'action': 'enter_app', 'params': '商旅', 'explain': None},
        {'step': 4, 'action': 'enter_menu', 'params': '整单方案,差旅申请单整单', 'explain': None},
        {'step': 5, 'action': 'create_bill', 'params': None, 'explain': None},
        {'step': 6, 'action': 'check_dim', 'params': None, 'explain': None},
        {'step': 7, 'action': 'add_dim_info', 'params': None, 'explain': None},
        {'step': 8, 'action': 'submit', 'params': None, 'explain': None},
    ]
    main(flow_path)

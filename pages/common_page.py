# -*- coding:utf-8 -*-
# @Time : 2021/5/11
# @Author : 张顺利
# @Group : 云业务测试部
# @Email : zhangshunl@yuanian.com
from selenium.webdriver.common.by import By
from frame.core.basepage import BasePage
from frame.core.decorators import keyword, switch_to_frame
from frame.utils.handle_log import log


class Location:
    username_box = (By.ID, 'e_username')  # 用户名输入框
    password_box = (By.ID, 'e_password')  # 密码输入框
    login_btn = (By.XPATH, '//span[text()="登 录"]/..')  # 登录按钮

    @classmethod
    def common_locator(cls, text):
        common_xpath = '//span[text()="{}"]'.format(text)
        common_loc = (By.XPATH, common_xpath)  # 应用菜单
        return common_loc


class Common(BasePage):
    @keyword()
    def login(self, username, password):
        self.driver.send_keys(Location.username_box, username)
        self.driver.send_keys(Location.password_box, password)
        self.driver.click(Location.login_btn)

    @keyword()
    def enter_app(self, title):
        self.driver.click(Location.common_locator(title))

    @keyword()
    @switch_to_frame()
    def enter_menu(self, level_1, level_2):
        level_1_loc = Location.common_locator(level_1)
        level_2_loc = Location.common_locator(level_2)
        self.driver.click(level_1_loc)
        self.driver.click(level_2_loc)



if __name__ == '__main__':
    pass




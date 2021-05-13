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
    create_bill_btn = (By.ID, 'd7f9728d48ae11eab6a44d20531b9c2d-createBill')  # 创建单据按钮
    dim_tag = (By.XPATH, "(//span[@class='no_special_readOnly_field_box'])[1]")  # 预算归属
    km_box = (By.XPATH, "(//span[@class='ant-select-selection__rendered'])[13]")  # 科目box
    search_box = (By.XPATH, "//input[@class='ant-select-search__field']")  # 搜索框
    cbf_tag = (By.XPATH, "//span[@class='ant-select-tree-title' and text()='机票费']")  # 差补费选项
    save_btn = (By.XPATH, "//button[@type='submit' and @class='ant-btn btn_space ant-btn-primary']")  # 保存按钮
    submit_btn = (By.ID, 'd7f9728d48ae11eab6a44d20531b9c2d-SUBMIT')  # 提交按钮

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

    @keyword()
    @switch_to_frame()
    def create_bill(self):
        self.driver.click(Location.create_bill_btn)

    @keyword()
    @switch_to_frame()
    def check_dim(self):
        self.driver.click(Location.dim_tag)

    @keyword()
    @switch_to_frame()
    def add_dim_info(self):
        self.driver.click(Location.km_box)
        self.driver.send_keys(Location.search_box, '机票费')
        self.wait(2)
        self.driver.click(Location.cbf_tag)
        self.wait(1)
        self.driver.click(Location.save_btn)

    @keyword()
    @switch_to_frame()
    def submit(self):
        self.driver.click(Location.submit_btn)


if __name__ == '__main__':
    pass




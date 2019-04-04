import unittest

from selenium.webdriver.common import keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """待办事项验证测试：测试表单输入数据的合规性"""

    def test_cannot_add_empty_list_items(self):
        """测试输入空内容"""
        # Edith访问首页
        self.browser.get(self.live_server_url)
        # 她在输入框中没有输入内容，就按下了回车
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(keys.Keys.ENTER)
        # 首页刷新了，显示一个错误消息（只有通过回车键或点击按钮提交表单后页面才会刷新）
        # 待办事项不能为空
        ## 使用一个显示等待方法，来等待页面刷新后是否有.has-error
        self.wait_for(lambda: self.assertEqual(
            # 通过CSS选择器查找错误文本（如果页面刷新，就要显示等待；否则Selenium可能会在页面加载之前查找.has-error元素
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an emtpy todo item"
        ))

        #
        # 她输入一些文字，然后再次提交，这次没问题了
        self.browser.find_element_by_id('id_new_item').send_keys('Buy some milk')
        self.browser.find_element_by_id('id_new_item').send_keys(keys.Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy some milk')

        # 她有点调皮，再次输入了一个空的待办事项
        self.browser.find_element_by_id('id_new_item').send_keys(keys.Keys.ENTER)
        # 她在待办事项列表页面中又看到了一条类似的错误信息
        self.wait_for(lambda: self.assertEqual(
            # 通过CSS选择器查找错误文本（如果页面刷新，就要显示等待；否则Selenium可能会在页面加载之前查找.has-error元素
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an emtpy todo item"
        ))
        # 再次输入内容后，就没问题了
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(keys.Keys.ENTER)
        self.wait_for_row_in_list_table("2: Make tea")
        self.wait_for_row_in_list_table("1: Buy some milk")

        # self.fail('Finish Test: Cannot add empty list item')
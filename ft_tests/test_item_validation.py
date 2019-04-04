import unittest

from selenium.webdriver.common import keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """待办事项测试"""

    @unittest.skip
    def test_cannot_add_empty_list_items(self):
        """测试输入空内容"""
        # Edith访问首页
        self.client.get(self.live_server_url)
        # 她在输入框中没有输入内容，就按下了回车
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(keys.Keys.ENTER)
        # 首页刷新了，显示一个错误消息
        # 待办事项不能为空

        self.fail('Finish Test: Cannot add empty list item')

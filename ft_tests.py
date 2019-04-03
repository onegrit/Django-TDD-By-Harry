import time

from selenium import webdriver
import unittest

from selenium.webdriver.common import keys


class NewVisitorTest(unittest.TestCase):  # 测试组织成类的形式，继承自TestCase
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """FT:用户使用待办事项功能"""
        # Edith 听说有一个很酷的在线待办事项应用
        # 她来到这个网站，首先看到了首页
        self.browser.get('http://localhost:8010')
        # 她注意到网页的标题和头部都包含“To-Do”这个词
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # 她在文本框中输入了“Buy peacock feathers” （购买孔雀羽毛）
        # 伊迪丝的爱好是使用假蝇做饵钓鱼
        input_box.send_keys('Buy peacock feathers')
        # 她按回车键后，页面更新了
        input_box.send_keys(keys.Keys.ENTER)
        time.sleep(1)
        # 在待办事项表格中显示了“1: Buy peacock feathers”
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        # #判断内容是否在表格的多个行中
        # self.assertTrue(
        #     any(row.text == "1: Buy peacock feathers" for row in rows),
        #     f"New to-do item did not appear in table. Contents were:\n{table.text}"  # assert×添加失败的消息
        # )
        # 重构上面的代码，修改为如下：
        self.assertIn("1: Buy peacock feathers", [row.text for row in rows])

        # 页面中又显示了一个文本框，可以输入其他待办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        # 她输入了“Use peacock feathers to make a fly” （使用孔雀羽毛做假蝇）
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(keys.Keys.ENTER)
        time.sleep(1)
        # Edith做事很有条理

        # 页面再次更新，在她的待办事项列表中显示了两个待办事项
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn("1: Buy peacock feathers", [row.text for row in rows])
        self.assertIn("2: Use peacock feathers to make a fly", [row.text for row in rows])

        self.fail('Finish the test!')

        # Edith想知道这个网站是否会记住她的清单（待办事项清单）
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 她访问这个URL，发现她的待办事项还在

        # 她很满意，去睡觉了


if __name__ == '__main__':
    unittest.main()

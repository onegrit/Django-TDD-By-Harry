import time

from django.test import LiveServerTestCase
from selenium import webdriver
import unittest

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import keys

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):  # 测试组织成类的形式，继承自TestCase
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """使用隐世等待方式，显示列表中的行,消除显示等待time.sleep"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """FT:用户使用待办事项功能"""
        # Edith 听说有一个很酷的在线待办事项应用
        # 她来到这个网站，首先看到了首页
        self.browser.get(self.live_server_url)
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
        # TODO:显示等待需要重构为隐示等待
        # time.sleep(1)
        # 重构显示等待time.sleep()
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        # 在待办事项表格中显示了“1: Buy peacock feathers”
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # 使用辅助方法重构上面两行
        # self.wait_for_row_in_list_table("1: Buy peacock feathers")
        # #判断内容是否在表格的多个行中
        # self.assertTrue(
        #     any(row.text == "1: Buy peacock feathers" for row in rows),
        #     f"New to-do item did not appear in table. Contents were:\n{table.text}"  # assert×添加失败的消息
        # )
        # 重构上面的代码，修改为如下：
        # self.assertIn("1: Buy peacock feathers", [row.text for row in rows])

        # 页面中又显示了一个文本框，可以输入其他待办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        # 她输入了“Use peacock feathers to make a fly” （使用孔雀羽毛做假蝇）
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(keys.Keys.ENTER)
        # time.sleep(1)
        # 重构显示等待time.sleep()
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        # Edith做事很有条理

        # 页面再次更新，在她的待办事项列表中显示了两个待办事项
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn("1: Buy peacock feathers", [row.text for row in rows])
        # self.assertIn("2: Use peacock feathers to make a fly", [row.text for row in rows])
        # 使用辅助方法重构上面4行
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        self.fail('Finish the test!')

    def test_multiple_user_can_start_lists_at_different_urls(self):
        """多个用户拥有自己的清单列表URL"""
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(keys.Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        # Edith想知道这个网站是否会记住她的清单（待办事项清单）
        # TODO: 全局清单，确保每人有自己的待办事项清单
        # Rep:想让每个用户都能保存自己的清单.SO: 若想查看某个清单，可以发送GET请求到URL： /lists/<list_id>/
        # 若想创建全新的清单，可以向/lists/new发送POST请求
        # 若想向现有清单中添加一个待办事项，可以想URL:/lists/<list_id>/add_item发送POST请求
        # 每个清单由待办事项组成，待办事项的主要属性应该是一些描述性文字
        # 要保存清单，以便多次访问。现在可以为用户提供一个唯一的URL，指向他们的清单。

        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # 现在一名叫做Francis的新用户访问了网站
        ## 我们要使用一个新浏览器会话
        ## 确保Edith的信息不会从Cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis 访问首页
        # 在页面中看不到Edith的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis 输入一个新待办事项，新建一个清单
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(keys.Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis 获得了她的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有Edith的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn("Buy milk", page_text)
        # 她访问这个URL，发现她的待办事项还在

        # 她很满意，去睡觉了

        # TODO：隔离功能测试【SOLVED】
        # 功能测试使用的是真正的数据库（不像单元测试），运行功能测试后，待办事项一直存在于数据库中，这会影响下次测试的结果；应确保功能测试之间相互隔离
        # 解决办法：使用LiveServerTestCase

from selenium import webdriver
import unittest


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
        # self.fail('Finish the test!')

        # 她在文本框中输入了“Buy peacock feathers” （购买孔雀羽毛）
        # 伊迪丝的爱好是使用假蝇做饵钓鱼

        # 她按回车键后，页面更新了
        # 在待办事项表格中显示了“1: Buy peacock feathers”

        # 页面中又显示了一个文本框，可以输入其他待办事项
        # 她输入了“Use peacock feathers to make a fly” （使用孔雀羽毛做假蝇）
        # Edith做事很有条理

        # 页面再次更新，在她的待办事项列表中显示了两个待办事项

        # Edith想知道这个网站是否会记住她的清单（待办事项清单）
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 她访问这个URL，发现她的待办事项还在

        # 她很满意，去睡觉了


if __name__ == '__main__':
    unittest.main()

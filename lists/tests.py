from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from .views import home_page
from .models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        """UT:确保视图函数返回正确的html"""
        response = self.client.get('/')  # 把HttpRequest交由视图函数处理，返回response

        html = response.content.decode('utf8')  # 解码response

        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('To-Do', html)
        self.assertTrue(html.endswith('</html>'))

    def test_uses_home_template(self):
        """UT:测试根路径URL使用了正确的模板"""
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        """"""
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_a_post_request(self):
        """前端UT:保存用户表单输入的POST请求数据"""
        self.client.post('/', data={'item_text': 'A new list item'})  # 此处的item_text是模板中input的name

        # 断言:POST后的数据数量
        self.assertEqual(Item.objects.count(), 1)

        # 断言：取出的数据和保存的数据是否相同
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        """UT:POST请求后应该重定向到list页面"""
        response = self.client.post('/', data={'item_text': 'A new list item'})  # 此处的item_text是模板中input的name

        # 重定向到列表页面
        # 断言：response的状态码
        self.assertEqual(response.status_code, 302)
        # 断言：response的location
        self.assertEqual(response['location'], '/')

    def test_displays_all_list_items(self):
        """UT：在表格中显示多个待办事项"""
        Item.objects.create(text='First item to do')
        Item.objects.create(text='Second item to do')

        response = self.client.get('/')

        self.assertIn('First item to do', response.content.decode())
        self.assertIn('Second item to do', response.content.decode())


class ItemModelTest(TestCase):
    """Model测试:待办事项"""

    def test_saving_and_retrieving_items(self):
        first_item = Item()  # 创建对象
        first_item.text = "The first list item"  # 为对象属性赋值
        first_item.save()

        second_item = Item()
        second_item.text = "The second list item"
        second_item.save()

        saved_items = Item.objects.all()  # 查询API，all是取回表中全部记录，得到的是类似列表的对象QuerySet
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_item, first_saved_item)
        self.assertEqual(second_saved_item, second_item)

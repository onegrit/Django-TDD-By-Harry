from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from .views import home_page
from .models import  Item


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

    def test_can_save_a_post_request(self):
        """UT:保存用户表单输入的POST请求"""
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


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

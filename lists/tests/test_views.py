from unittest import skip

from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):
    # @skip
    # def test_home_page_returns_correct_html(self):
    #     """UT:确保视图函数返回正确的html"""
    #     response = self.client.get('/')  # 把HttpRequest交由视图函数处理，返回response
    #
    #     html = response.content.decode('utf8')  # 解码response
    #
    #     self.assertTrue(html.startswith('<!DOCTYPE html>'))
    #     self.assertIn('To-Do', html)
    #     self.assertTrue(html.endswith('</html>'))

    def test_uses_home_template(self):
        """UT:测试根路径URL使用了正确的模板"""
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_displays_only_items_for_that_list(self):
        """UT：相互独立的待办事项清单列表"""
        correct_list = List.objects.create()
        Item.objects.create(text='First item to do', list=correct_list)
        Item.objects.create(text='Second item to do', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='Other  item to do 1', list=other_list)
        Item.objects.create(text='Other  item to do 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'First item to do')
        self.assertContains(response, 'Second item to do')
        self.assertNotContains(response, 'Other  item to do 1')
        self.assertNotContains(response, 'Other  item to do 2')

    def test_use_list_template(self):
        a_list = List.objects.create()
        response = self.client.get(f'/lists/{a_list.id}/')

        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        """列表视图向模板传递正确的清单id"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    def test_can_save_a_post_request(self):
        """前端UT:保存用户表单输入的POST请求数据"""
        a_list = List.objects.create()
        self.client.post('/lists/new',
                         data={'item_text': 'A new list item', 'list': a_list})  # 此处的item_text是模板中input的name

        # 断言:POST后的数据数量
        self.assertEqual(Item.objects.count(), 1)

        # 断言：取出的数据和保存的数据是否相同
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        """UT:POST请求后应该重定向到list页面"""
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})  # 此处的item_text是模板中input的name
        new_list = List.objects.first()

        # 重定向到列表页面
        # 断言：response的状态码
        # self.assertEqual(response.status_code, 302)
        # 断言：response的location
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        # 重构：使用assertRedirect重构上面的代码
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    def test_can_save_a_post_request_to_an_existing_list(self):
        """UT:新的待办事项能够添加到已存在清单中"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """POST后重定向到新的列表视图"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

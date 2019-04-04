from unittest import skip

from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    """Model测试:待办事项"""

    def test_saving_and_retrieving_items(self):
        a_list = List()
        a_list.save()

        first_item = Item()  # 创建对象
        first_item.text = "The first list item"  # 为对象属性赋值
        first_item.list = a_list
        first_item.save()

        second_item = Item()
        second_item.text = "The second list item"
        second_item.list = a_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, a_list)

        saved_items = Item.objects.all()  # 查询API，all是取回表中全部记录，得到的是类似列表的对象QuerySet
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_item, first_saved_item)
        self.assertEqual(first_item.list, a_list)
        self.assertEqual(second_saved_item, second_item)
        self.assertEqual(second_item.list, a_list)

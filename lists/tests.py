from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from .views import home_page


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

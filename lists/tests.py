from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from .views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        """UT路由解析:能否解析网站根路径'/'，并将其对应到某个视图函数上"""
        # resolve是Django的内部函数，用于解析URL，并将其映射到相应的视图函数中。检查解析网站根路径"/"时，是否能找到名为home_page的函数
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """UT:视图函数返回正确的html"""
        request = HttpRequest()  # 构建一个HttpRequest请求
        response = home_page(request)  # 把HttpRequest交由视图函数处理，返回response
        html = response.content.decode('utf8')  # 解码response

        self.assertTrue(html.startswith('<html>'))
        self.assertIn('To-Do', html)
        self.assertTrue(html.endswith('</html>'))

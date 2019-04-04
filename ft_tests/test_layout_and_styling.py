from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    """布局和样式测试"""

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)

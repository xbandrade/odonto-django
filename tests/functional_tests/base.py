import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import make_chrome_browser


class BaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, sec=2):  # pragma: no cover
        time.sleep(sec)

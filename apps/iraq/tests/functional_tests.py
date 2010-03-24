from unittest import TestCase
from selenium.firefox.webdriver import WebDriver

class HomePageTest(TestCase):

    def _load_home_page(self):
        self.driver.get("http://127.0.0.1:8000/charts")
        
    def test_get_title(self):
        self.driver = WebDriver()
        self._load_home_page()
        title = self.driver.get_title()
        self.assertEquals("foobar", title)

    def tearDown(self):
        self.driver.quit()

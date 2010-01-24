from django.test import TestCase
from register.app import App
from rapidsms.tests.scripted import TestScript
from register.models import *
from rapidsms import *

class RegisterTest(TestCase):
    def test_register_needs_a_keyword_at_the_start_of_the_message(self):
        app = App(None)
        result = app.handle(Message(text="regirrt 100 1001 poll", connection=1000))
        self.assertEquals(result, None)
        result = app.handle(Message(text="register 100 1001 poll", connection=1000))
        self.assertEquals(result, True)
        

class TestRegister (TestScript):
    apps = (App,)

    test_register_needs_a_keyword_at_the_start_of_the_message = """
      03948 > register 100 1001 poll
      03948 < Thanks for registering for the survey.
      """

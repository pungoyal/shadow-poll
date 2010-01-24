from django.test import TestCase
from register.app import App
from rapidsms.tests.scripted import TestScript
from register.models import *
from rapidsms import *
from rapidsms.connection import *

class RegisterTest(TestCase):
    def test_register_needs_a_keyword_at_the_start_of_the_message(self):
        app = App(None)
        result = app.handle(Message(text="regirrt poll 100 1001", connection=1000))
        self.assertEquals(result, None)
        result = app.handle(Message(text="register poll 100 1001", connection=Connection(backend = None, identity=1000)))
        self.assertEquals(result, True)
        

class TestRegister (TestScript):
    apps = (App,)

    test_register_needs_a_keyword_at_the_start_of_the_message = """
      03948 > register poll 100 1001
      03948 < Thanks for registering for the survey.
      """

    error_message = "We could not understand the register message. Please send as - register survey governorate district"
    test_incomplete_information_passed_in_the_register_message = """
      1000 > register poll 10001000
      1000 < %s
      1000 > register
      1000 < %s
      """ % (error_message, error_message)
    
class RegistrationTest(TestCase):
    def test_parse(self):
        reg = Registration(number = 1000)
        reg.parse('register poll 100 1001')
        self.assertEquals(reg.public_identifier, 'poll')
        self.assertEquals(reg.governorate, '100')
        self.assertEquals(reg.district, '1001')
        self.assertEquals(reg.number, 1000)
    

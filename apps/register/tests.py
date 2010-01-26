# -*- coding: utf-8 -*-
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
        result = app.handle(Message(text="register", connection=1000))
        self.assertEquals(result, True)
        result = app.handle(Message(text="register poll", connection=1000))
        self.assertEquals(result, True)

        result = app.handle(Message(text="register poll 100 1001", connection=Connection(backend = None, identity=1000)))
        self.assertEquals(result, True)
        

class TestRegisterScript (TestScript):
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
      90800 > register ومساحتها
      90800 < %s
      """ % (error_message, error_message, error_message)
    
class RegistrationTest(TestCase):
    def test_parse(self):
        reg = Registration(mobile_number = 1000)
        reg.parse('register poll 100 1001')
        self.assertEquals(reg.public_identifier, 'poll')
        self.assertEquals(reg.governorate, '100')
        self.assertEquals(reg.district, '1001')
        self.assertEquals(reg.mobile_number, 1000)

    def test_load_by_mobile_number(self):
        r = Registration.objects.filter(mobile_number = 1000)

    def test_to_string(self):
        r = Registration(mobile_number = 1000)
        r.public_identifier = "Poll"
        r.governorate = "Baghdad"
        r.district = "Baghdad"

        self.assertEquals(str(r), "1000 Poll Baghdad Baghdad")

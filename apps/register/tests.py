# -*- coding: utf-8 -*-
from django.test import TestCase
from rapidsms import *
from rapidsms.connection import *
from rapidsms.tests.scripted import TestScript
from register.models import *
from reporters.models import PersistantBackend, Reporter
from register.app import App
from poll.models import Phone
import poll.app as poll_app
import register.app as register_app
import reporters.app as reporter_app

class TestRegisterScript (TestScript):
    apps = (poll_app.App, register_app.App, reporter_app.App)

    def setUp(self):
        TestScript.setUp(self)

    test_register_needs_keyword_at_the_start_of_the_message_rapidsms = """
      03948 > register poll 100 1001
      03948 < Thanks for registering for the survey.
      """

    error_message = "We could not understand the register message. Please send as - register survey governorate district"
    test_incomplete_information_passed_in_the_register_message = """
      1000 > register poll 10001000
      1000 < %(error_msg)s
      1000 > register
      1000 < %(error_msg)s
      90800 > register ومساحتها
      90800 < %(error_msg)s
      """ % {"error_msg":error_message}
    
class TestRegisterArabicScript (TestScript):
    apps = (poll_app.App, register_app.App, reporter_app.App)

    def setUp(self):
        TestScript.setUp(self)

    fails_test_registration_message_in_arabic = u"""
        1000 > تسجيل التصويت 100 1001
        1000 < شكراً لتسجيلك في  هذه الدراسة
    """
    
    fails_arabic_error_message = u"لم نستطيع فهم الرسالة المسجلة, الرجاء إرسال - التسجيل  الدراسة  المحافظة  الحي"
    test_incomplete_information_passed_in_the_register_message_arabic = u"""
        1000 > regحتister
        1000 < %(error_msg)s
        90800 > register ومساحتها
        90800 < %(error_msg)s
    """ % {"error_msg":arabic_error_message}

class RegisterTest(TestCase):
    def test_register_needs_keyword_at_the_start_of_the_message_base(self):
        app = App(None)
        result = app.handle(Message(text="regirrt poll 100 1001", connection=1000))
        self.assertEquals(result, None)
        result = app.handle(Message(text="register", connection=1000))
        self.assertEquals(result, True)
        result = app.handle(Message(text="register poll", connection=1000))
        self.assertEquals(result, True)

        result = app.handle(Message(text="register poll 100 1001", connection=Connection(backend = None, identity=1000)))
        self.assertEquals(result, True)
        
class RegistrationTest(TestCase):
    fixtures = ['registration']
    
    def setUp(self):
        self.backend = PersistantBackend(slug="MockBackend")
        self.backend.save()
        self.reporter = Reporter(alias="ReporterName")
        self.reporter.save()
        self.connection = Connection(backend=self.backend, identity="1000")
        self.pconnection = Phone(backend=self.backend, 
                                 reporter=self.reporter, 
                                 identity="1000")
        self.pconnection.save()
        self.reporter.connections.add(self.pconnection)
        
        self.reg = Registration()
        message = Message(text='register poll 100 1001', connection=self.connection)
        message.persistant_connection = self.pconnection
        self.reg.parse(message)

    
    def test_parse(self):
        self.assertEquals(self.reg.public_identifier, 'poll')
        self.assertEquals(self.reg.governorate, '100')
        self.assertEquals(self.reg.district, '1001')
        self.assertEquals(self.reg.phone.identity, "1000")

    def test_load_by_mobile_number(self):
        query_result = Registration.objects.filter(phone__identity = '100')
        self.assertEquals(query_result.count(), 0)

        query_result = Registration.objects.filter(phone__identity = '1000')
        self.assertEquals(query_result.count(), 1)
        r = query_result.iterator().next()
        self.assertNotEquals(r, None)

    def test_to_string(self):
        r = Registration()
        r.public_identifier = "Poll"
        r.governorate = "12"
        r.district = "8"
        r.phone = self.pconnection
        self.assertEquals(str(r), "1000 Poll 12 8")

# -*- coding: utf-8 -*-
#imports for functional tests
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
#model and app tests
from subtests.models import *
from subtests.app import *


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
      """ % {"error_msg":error_message}
    
class TestRegisterArabicScript (TestScript):
    apps = (poll_app.App, register_app.App, reporter_app.App)

    def setUp(self):
        TestScript.setUp(self)

    test_registration_message_in_arabic = u"""
        1000 > تسجيل التصويت 100 1001
        1000 < شكراً لتسجيلك في  هذه الدراسة
    """
    
    arabic_error_message = u"لم نستطيع فهم الرسالة المسجلة, الرجاء إرسال - التسجيل  الدراسة  المحافظة  الحي"
    # the first case doesn't return anything since it falls through the register app
    test_incomplete_information_passed_in_the_register_message_arabic = u"""
        1000 > regحتister
        1000 > register ومساحتها
        1000 < %(error_msg)s
    """ % {"error_msg":arabic_error_message}


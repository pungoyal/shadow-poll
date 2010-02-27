#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from apps.reporters.app import App as reporter_app
from apps.default.app import App as default_app
from apps.register.app import App as register_app
from apps.internationalization.app import App as i18n_app
from rapidsms.tests.scripted import TestScript
from apps.poll.app import App as poll_app

class TestIntegration(TestScript):
    """ Test our various SMS apps all together now """
    fixtures = ['poll_interactive.json']
    apps = (reporter_app, register_app, default_app, i18n_app, poll_app)

    test_arabic_error_when_given_random_junk = u"""
        00919980131127 > تصويت
        00919980131127 < لقد اخترت خيارا غير موجودة ، يرجى اختيار واحد من بين الخيارات المذكورة سابقاً
    """
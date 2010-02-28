#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from apps.reporters.app import App as reporter_app
from apps.default.app import App as default_app
from apps.register.app import App as register_app
from apps.internationalization.app import App as i18n_app
from rapidsms.tests.scripted import TestScript
from apps.poll.app import App as poll_app

class TestIntegration_2(TestScript):
    """ Test our various SMS apps all together now """
    fixtures = ['poll_interactive.json']
    apps = (reporter_app, register_app, default_app, i18n_app, poll_app)

    test_arabic_error_when_given_random_junk = u"""
        00919980131127 > تصويت
        00919980131127 <   انا أشعر بالسعادة : (الرجاء إختيار أ,ب,ج  أو د)   أ.دائماً    ب.معظم الوقت    ج. نادراً    د.لا أشعر بالسعادة أبداً
    """

    test_error_when_given_random_junk = u"""
        00919980131127 > junk
        00919980131127 <  I feel happy: (Choose a,b,c or d.) a. Always b. Most of the time c. Rarely d. Never
    """

#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

""" 

This is an integration test suite for the internationalization app.
Its purpose is to make sure that this app plays nicely with other apps.

"""

from rapidsms.tests.scripted import TestScript

import apps.internationalization.app as internationalization_app
import apps.logger.app as logger_app
import apps.echo.app as echo_app
from apps.logger.models import IncomingMessage, OutgoingMessage

class TestSchedule (TestScript):
    apps = (internationalization_app.App, logger_app.App, echo_app.App)
    
    def setUp(self):
        TestScript.setUp(self)
    
    def test_arabic_incoming_message_logged(self):
        """ Inject random arabic and make sure random arabic comes back out """
        arabic_input = u"التصويت"
        script = u"""
            1250 > %(input)s
            1250 < ARABICYou ARABICsaid: ARABICpoll
        """ % {'input':arabic_input}
        self.runScript(script)
        logged_message = IncomingMessage.objects.all().order_by('-received')[0]
        self.assertEquals(logged_message.text, arabic_input)
        
    def test_arabic_outgoing_message_logged(self):
        """ Inject random arabic and make sure random arabic comes back out """
        arabic_response = u"ARABICYou ARABICsaid: ARABICpoll"
        script = u"""
            1250 > التصويت
            1250 < %(response)s
        """ % {'response':arabic_response}
        self.runScript(script)
        logged_message = OutgoingMessage.objects.all().order_by('-sent')[0]
        self.assertEquals(logged_message.text, arabic_response)
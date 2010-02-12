#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from datetime import datetime, timedelta
from django.test import TestCase as DjTestScript
from rapidsms.tests.scripted import TestScript
import apps.logger.app as logger_app
import apps.reporters.app as reporters_app
import apps.default.app as default_app
from apps.default.app import _test_and_set_bot
from apps.reporters.models import PersistantConnection, PersistantBackend
from apps.logger.models import IncomingMessage
 
class TestSMSCommands (TestScript):
    apps = (logger_app.App, reporters_app.App, default_app.App )

    def setUp(self):
        TestScript.setUp(self)
        
    test_ignore_after_4_of_the_same = """
        8005551210 > junk
        8005551210 < We didn't understand your response.
        8005551210 > junk
        8005551210 < We didn't understand your response.
        8005551210 > junk
        8005551210 < We didn't understand your response.
        8005551210 > junk
        8005551210 < 
        8005551210 > junk
        8005551210 < 
        8005551210 > junk
        8005551210 < 
        8005551210 > junk
        8005551210 < 
        """

    test_do_not_ignore_after_4_different = """
        8005551210 > junk 1
        8005551210 < We didn't understand your response.
        8005551210 > junk 2
        8005551210 < We didn't understand your response.
        8005551210 > junk 3
        8005551210 < We didn't understand your response.
        8005551210 > junk 4
        8005551210 < We didn't understand your response.
        8005551210 > junk 5
        8005551210 < We didn't understand your response.
        8005551210 > junk 6
        8005551210 < We didn't understand your response.
        """

    test_some_different_some_same = """
        8005551210 > junk 1
        8005551210 < We didn't understand your response.
        8005551210 > junk
        8005551210 < We didn't understand your response.
        8005551210 > junk
        8005551210 < We didn't understand your response.
        8005551210 > junk 4
        8005551210 < We didn't understand your response.
        8005551210 > junk
        8005551210 < We didn't understand your response.
        8005551210 > junk
        8005551210 < We didn't understand your response.
        8005551210 > junk
        8005551210 < We didn't understand your response.
        8005551210 > junk
        8005551210 < 
        8005551210 > junk
        8005551210 < 
        """

class TestBot(DjTestScript):
    def setUp(self):
        self.backend = PersistantBackend(slug="MockBackend")
        self.backend.save()
        self.conn = PersistantConnection(backend=self.backend, 
                                                identity="1000")
        self.conn.save()
    
    def test_ignore_before_timeout(self):
        for i in range(0,5):
            IncomingMessage(text="123",identity=str(self.conn.identity), 
                            backend=str(self.conn.backend), 
                            received=datetime.now()).save()
        # this is a bot
        self.assertTrue( _test_and_set_bot(self.conn) )

    def test_allow_after_timeout(self):
        for i in range(0,5):
            IncomingMessage(text="123",identity=str(self.conn.identity), 
                            backend=str(self.conn.backend), 
                            received=datetime.now() - timedelta(minutes=5)
                            ).save()
        # this is not a bot
        self.assertFalse( _test_and_set_bot(self.conn) )

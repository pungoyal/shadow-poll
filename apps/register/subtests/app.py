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

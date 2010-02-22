from django.test import TestCase
from rapidsms.tests.scripted import TestScript
from poll.app import App as poll_App
import reporters.app as reporters_app
import internationalization.app as i18n_app
from poll.models import *
from reporters.models import Reporter, PersistantConnection, PersistantBackend
import unittest

class UserSessionTest(TestCase):
    apps = (poll_App,)

    def setUp(self):
        self.backend = PersistantBackend(slug="MockBackend")
        self.backend.save()
        self.reporter = Reporter(alias="ReporterName")
        self.reporter.save()
        self.pconnection = PersistantConnection(backend=self.backend, 
                                                reporter=self.reporter, 
                                                identity="1000")
        self.pconnection.save()
        self.reporter.connections.add(self.pconnection)
        
        self.question1 = Question(text = "question1")
        self.question1.save()
        self.question2 = Question(text = "question2")
        self.question2.save()
        self.question3 = Question(text = "question3")
        self.question3.save()
        
        self.question1.next_question = self.question2
        self.question2.next_question = self.question3

        self.question1.save()
        self.question2.save()
        self.question3.save()
        

    def test_open_new_session(self):
        self.question1 = Question(text = "question1")
        self.question1.is_first = True
        self.question1.save()
        
        self.session = UserSession.open(self.pconnection)
        self.assertEquals(self.session.question, self.question1)

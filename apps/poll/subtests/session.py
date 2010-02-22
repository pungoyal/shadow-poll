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
        
        self.questionnaire = Questionnaire()
        self.question1 = Question("question1")
        self.question2 = Question("question2")
        self.question3 = Question("question3")
        self.questionnaire.addQuestion(self.question1)
        self.questionnaire.addQuestion(self.question2)
        self.questionnaire.addQuestion(self.question3)
        self.questionnaire.save()

    def testOpenNewSession(self):
        self.session = UserSession.open(self.pconnection)
        self.assertEquals(self.session.questionnaire, self.questionnaire)
        self.assertEquals(self.session.question, None)
        


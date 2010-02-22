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
        self.question1.is_first = True
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

        self.setup_choices(self.question1)
        self.setup_choices(self.question2)
        self.setup_choices(self.question3)

        Questionnaire(trigger = "trigger").save()

    def setup_choices(self,question):
        choice1 = Choice(code= 'a',question=question)
        choice2 = Choice(code= 'b',question=question)
        choice3 = Choice(code= 'c',question=question)
        choice1.save()
        choice2.save()
        choice3.save()

    def test_open_new_session(self):
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.question, None)

        
    def test_respond_with_first_question_on_new_session_for_any_message(self):
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.respond("text"), "question1")

    def test_correct_response_to_question_sends_next_question(self):
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.question, None)
        response1 = session.respond("text")
        self.assertEquals(session.question, self.question1)
        response2 = session.respond("a")
        self.assertEquals(response2, "question2")
        self.assertEquals(session.question, self.question2)

    def test_wrong_response_to_question_sends_error(self):
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.question, None)
        response1 = session.respond("text")
        self.assertEquals(session.question, self.question1)
        response2 = session.respond("django")
        self.assertEquals(response2, "error_parsing_response")
        self.assertEquals(session.question, self.question1)

    def test_retrieve_ongoing_session_at_question2(self):
        session = UserSession.open(self.pconnection)
        session.question = self.question2
        session.save()
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.respond("c"), self.question3.text)
        self.assertEquals(session.question, self.question3)
        
    def test_close_ongoing_session_at_trigger(self):
        session = UserSession.open(self.pconnection)
        session.question = self.question2
        session.save()
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.respond("c"), self.question3.text)
        self.assertEquals(session.question, self.question3)
        
        self.assertEquals(session.respond("trigger"), self.question1.text)
        self.assertEquals(session.question, self.question1)


    def test_close_session_on_last_answer(self):
        session = UserSession.open(self.pconnection)
        session.question = self.question3
        self.assertEquals(session.respond("c"), "thanks")
        self.assertEquals(session.question, None)


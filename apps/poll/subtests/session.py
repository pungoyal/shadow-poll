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

        self.pconnection1 = PersistantConnection(backend=self.backend, 
                                                reporter=self.reporter, 
                                                identity="10001")
        self.pconnection1.save()

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

        q = Questionnaire(trigger = "trigger", max_retries=3)
        q.save()
        DemographicParser(questionnaire=q, name='age', regex='[0-9]+', 
                        order=1, type='i').save()
        DemographicParser(questionnaire=q, name='gender', 
                        regex='m|f|male|female', order=2, type='c').save()
        self.user = User(connection = self.pconnection)
        self.user.save()

    def setup_choices(self,question):
        choice1 = Choice(code= 'a',question=question, text="a")
        choice2 = Choice(code= 'b',question=question, text="a")
        choice3 = Choice(code= 'c',question=question, text="a")
        choice1.save()
        choice2.save()
        choice3.save()

    def test_open_new_session(self):
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.question, None)

        
    def test_respond_with_first_question_on_new_session_for_any_message(self):
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.respond("text"), str(self.question1))

    def test_correct_response_to_question_sends_next_question(self):
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.question, None)
        response1 = session.respond("text")
        self.assertEquals(session.question, self.question1)
        response2 = session.respond("a")
        self.assertEquals(response2, str(self.question2))
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
        session.user = self.user
        session.question = self.question2
        session.save()
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.respond("b"), str(self.question3))
        self.assertEquals(session.question, self.question3)
        
    def test_close_ongoing_session_at_trigger(self):
        session = UserSession.open(self.pconnection)
        session.user = self.user
        session.question = self.question2
        session.save()
        session = UserSession.open(self.pconnection)
        self.assertEquals(session.respond("c"), str(self.question3))
        self.assertEquals(session.question, self.question3)
        
        self.assertEquals(session.respond("trigger"), str(self.question1))
        self.assertEquals(session.question, self.question1)


    def test_close_session_on_last_answer(self):
        session = UserSession.open(self.pconnection)
        session.question = self.question3
        session.user  = self.user
        self.assertEquals(session.respond("c"), "thanks")
        self.assertEquals(session.question, None)


    def test_user_interaction_is_saved_when_successful(self):
        initial_number_of_responses = len(UserResponse.objects.all())
        initial_number_of_users = len(User.objects.all())
        
        session = UserSession.open(self.pconnection1)
        session.respond('trigger')
        self.assertEquals(len(User.objects.all()), initial_number_of_users + 1)
        session.respond('a')
        self.assertEquals(len(UserResponse.objects.all()), initial_number_of_responses + 1)

    def test_end_session_on_reaching_max_num_allowed_retries(self):
        session = UserSession.open(self.pconnection1)
        session.question = self.question1
        session.user = self.user
        session.respond('t')
        session.respond('t')
        session.respond('t')
        self.assertEquals(session.question, None)

    def test_user_demographics_saved_when_present(self):
        session = UserSession.open(self.pconnection1)
        session.respond('trigger 13 f')
        latest_user = User.objects.all().order_by('-id')[0]
        self.assertEquals(latest_user.age, 13)
        self.assertEquals(latest_user.gender, 'f')
        
        

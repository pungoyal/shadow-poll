from django.test import TestCase
from poll.app import App as poll_App
from poll.models import *
from reporters.models import Reporter, PersistantConnection, PersistantBackend

class UserSessionTest(TestCase):
    apps = (poll_App,)

    def setUp(self):
        # set up persistant connection
        self.backend = PersistantBackend(slug="MockBackend")
        self.backend.save()
        self.reporter = Reporter(alias="ReporterName")
        self.reporter.save()
        self.pconnection = PersistantConnection(backend=self.backend, 
                                                reporter=self.reporter, 
                                                identity="1000")
        self.pconnection.save()
        self.reporter.connections.add(self.pconnection)
        
        # create questionnaire
        q = Questionnaire(trigger = "poll")
        q.save()
        DemographicData(questionnaire=q, name='age', regex='[0-9]+', 
                        order=1, type='i').save()
        DemographicData(questionnaire=q, name='gender', 
                        regex='m|f|male|female', order=2, type='c').save()
        
        # initiate session
        self.session = UserSession.open(self.pconnection)
        self.session.questionnaire = q

    def test_trigger(self):
        self.session._save_user('poll')
        self.assertTrue(self.session.user is not None)
        self.assertEquals(self.session.user.age, None)
        self.assertEquals(self.session.user.gender, None)

    def test_trigger_age(self):
        self.session._save_user('poll 10')
        self.assertTrue(self.session.user is not None)
        self.assertEquals(self.session.user.age, 10)
        self.assertEquals(self.session.user.gender, None)

    def test_trigger_gender(self):
        self.session._save_user('poll f')
        self.assertTrue(self.session.user is not None)
        self.assertEquals(self.session.user.age, None)
        self.assertEquals(self.session.user.gender, 'f')

    def test_trigger_age_gender(self):
        self.session._save_user('poll 15 male')
        self.assertTrue(self.session.user is not None)
        self.assertEquals(self.session.user.age, 15)
        self.assertEquals(self.session.user.gender, 'm')

    def test_trigger_gender_age(self):
        self.session._save_user('poll female 100')
        self.assertTrue(self.session.user is not None)
        self.assertEquals(self.session.user.age, 100)
        self.assertEquals(self.session.user.gender, 'f')
        
    def test_trigger_junk(self):
        self.session._save_user('poll feeemale 100a')
        self.assertTrue(self.session.user is not None)
        self.assertEquals(self.session.user.age, None)
        self.assertEquals(self.session.user.gender, None)
        
    def test_trigger_age_junk(self):
        self.session._save_user('poll 14 asdf')
        self.assertTrue(self.session.user is not None)
        self.assertEquals(self.session.user.age, 14)
        self.assertEquals(self.session.user.gender, None)
        
    def test_trigger_gender_junk(self):
        self.session._save_user('poll f 234a')
        self.assertTrue(self.session.user is not None)
        self.assertEquals(self.session.user.age, None)
        self.assertEquals(self.session.user.gender, 'f')
        

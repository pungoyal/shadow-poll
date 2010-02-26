from django.test import TestCase
from apps.poll.models import *
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend

class DemographicParserTest(TestCase):
    def setUp(self):
        q = Questionnaire() 
        ageParser = DemographicParser(questionnaire=q, name='age', regex='[0-9]+', 
                        order=1, type='i')
        genderParser = DemographicParser(questionnaire=q, name='gender', 
                        regex='m|f|male|female', order=2, type='c')

        self.parsers = [ageParser, genderParser]

    def parse_using_parsers(self, message, user):
        for parser in self.parsers:
            parser.parse_and_set(message, user)

    def test_trigger(self):
        user = User()
        self.parse_using_parsers('poll', user)
        self.assertEquals(user.age, None)
        self.assertEquals(user.gender, None)

    def test_trigger_age(self):
        user = User()
        self.parse_using_parsers('poll 10', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, 10)
        self.assertEquals(user.gender, None)

    def test_trigger_gender(self):
        user = User()
        self.parse_using_parsers('poll f', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, None)
        self.assertEquals(user.gender, 'f')

    def test_trigger_age_gender(self):
        user = User()
        self.parse_using_parsers('poll 15 male', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, 15)
        self.assertEquals(user.gender, 'm')

    def test_trigger_Gender_age(self):
        user = User()
        self.parse_using_parsers('poll Male 10', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, 10)
        self.assertEquals(user.gender, 'm')

        user = User()
        self.parse_using_parsers('poll Female 10', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, 10)
        self.assertEquals(user.gender, 'f')

    def test_trigger_gender_age(self):
        user = User()
        self.parse_using_parsers('poll female 100', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, 100)
        self.assertEquals(user.gender, 'f')

    def test_trigger_junk(self):
        user = User()
        self.parse_using_parsers('poll make 10', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, 10)
        self.assertEquals(user.gender, None)

        user = User()
        self.parse_using_parsers('poll feeemale 100a', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, None)
        self.assertEquals(user.gender, None)

    def test_trigger_age_junk(self):
        user = User()
        self.parse_using_parsers('poll 14 asdf', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, 14)
        self.assertEquals(user.gender, None)
        
    def test_trigger_gender_junk(self):
        user = User()
        self.parse_using_parsers('poll f 234a', user)
        self.assertTrue(user is not None)
        self.assertEquals(user.age, None)
        self.assertEquals(user.gender, 'f')
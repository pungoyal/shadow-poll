from apps.poll.models import *
from poll.app import App as poll_app
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend
from rapidsms.tests.scripted import TestScript
from math import fsum

class StatsTest(TestScript):
    fixtures = ['functional_test_data.json', 'poll_interactive']
    apps = (poll_app,)
    
    def test_response_break_up(self):
        self.assertNotEquals(len(UserResponse.objects.all()), 0)

        question = Question.objects.get(id=1)
        break_up = question.response_break_up()

        self.assertEquals(break_up[0], 33.3)
        self.assertEquals(break_up[1], 29.2)
        self.assertEquals(break_up[2], 16.7)
        self.assertEquals(break_up[3], 20.8)

    def test_sum_of_break_up_values_should_be_100(self):
        question = Question(id=1)
        break_up = question.response_break_up()

        self.assertEquals(fsum(break_up), 100)

    def test_most_voted_option_in_loc(self):
        question = Question(id=1)
        choice = question.most_voted_choice_by_governorate(governorate_id=1)
        self.assertEquals(choice.text, "Always")
        choice = question.most_voted_choice_by_governorate(governorate_id=5)
        self.assertEquals(choice, None)

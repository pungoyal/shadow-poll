from apps.poll.models import *
from poll.app import App as poll_app
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend
from rapidsms.tests.scripted import TestScript
try:
    from math import fsum
except Exception, e:
    pass

class StatsTest(TestScript):
    fixtures = ['functional_test_data.json', 'poll_interactive']
    apps = (poll_app,)
    
    def test_response_break_up(self):
        self.assertNotEquals(len(UserResponse.objects.all()), 0)

        question = Question.objects.get(id=1)
        break_up = question.response_break_up()

        self.assertEquals(break_up[0], 14.9)
        self.assertEquals(break_up[1], 55.3)
        self.assertEquals(break_up[2], 6.4)
        self.assertEquals(break_up[3], 23.4)

    def test_sum_of_break_up_values_should_be_100(self):
        question = Question(id=1)
        break_up = question.response_break_up()
        
        try:
            self.assertEquals(fsum(break_up), 100)
        except NameError:
            # TODO - put some equivalent test here
            pass

    def test_most_voted_category_in_loc(self):
        question = Question(id=1)
        category = question.most_voted_category_by_governorate(governorate_id=1)
        self.assertEquals(category, None)
        category = question.most_voted_category_by_governorate(governorate_id=5)
        self.assertEquals(category.name, 'Always')

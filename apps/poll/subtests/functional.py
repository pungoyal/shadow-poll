from apps.poll.models import *
from apps.charts.models import Governorate
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend
from django.test import TestCase

class StatsTest(TestCase):
    fixtures = ['functional_test_data.json']

    def test_response_break_up(self):
        self.assertNotEquals(len(UserResponse.objects.all()), 0)

        question = Question.objects.get(id=1)
        break_up = question.response_break_up()
        choices = Choice.objects.filter(question=question).order_by('id')

        self.assertEquals(break_up[0]['text'], u'Most of the time')

        self.assertEquals(break_up[1]['percentage'], 14.9)
        self.assertEquals(break_up[2]['percentage'], 55.3)
        self.assertEquals(break_up[3]['percentage'], 23.4)
        self.assertEquals(break_up[4]['percentage'], 6.4)

    def test_sum_of_break_up_values_should_be_100(self):
        question = Question.objects.get(id=1)
        break_up = question.response_break_up()

        sum=0
        for group in break_up[1:]:
            sum += group['percentage']
        self.assertEquals(sum, 100)

    def test_most_voted_category_in_loc(self):
        question = Question(id=1)
        governorate = Governorate.objects.get(id=1)
        category = governorate.most_voted_category()
        self.assertEquals(category, None)
        governorate = Governorate.objects.get(id=5)
        category = governorate.most_voted_category()
        self.assertEquals(category.name, 'Always')

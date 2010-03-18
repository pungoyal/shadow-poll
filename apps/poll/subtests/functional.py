from apps.poll.models import *
from apps.charts.models import Governorate
from apps.reporters.models import Reporter, PersistantConnection, PersistantBackend
from django.test import TestCase

class StatsTest(TestCase):
    fixtures = ['functional_test_data.json']

    def test_most_voted_category_in_loc(self):
        question = Question(id=1)
        governorate = Governorate.objects.get(id=1)
        category = governorate.most_popular_category(question,{'gender': u'm,f', 'age': u'a1,a2,a3'})
        self.assertEquals(category, None)
        governorate = Governorate.objects.get(id=5)
        category = governorate.most_popular_category(question,{'gender': u'm,f', 'age': u'a1,a2,a3'})
        self.assertEquals(category.name, 'Always')

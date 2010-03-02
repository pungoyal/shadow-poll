from django.test import TestCase, Client
from poll.models import Question
from charts.models import Governorate

class ViewTests(TestCase):
    
    fixtures = ['functional_test_data']
    def setUp(self):
        self.client = Client()        

    def test_urls_are_set_up_properly(self):
        self.assertEquals(self.client.get('/charts/').status_code, 200)
        questions = Question.objects.all()
        governorates = Governorate.objects.all()
        for question in questions:
            url = '/charts/question%s' % question.id
            self.assertEquals(self.client.get(url).status_code, 200)
            for governorate in governorates:
                url = '/charts/%s/question%s' % (governorate.id, question.id)
                self.assertEquals(self.client.get(url).status_code, 200)

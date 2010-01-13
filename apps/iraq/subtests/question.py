from django.test import TestCase
import rapidsms
from iraq.models import *

class QuestionTest(TestCase):
    fixtures = ['question']
    def test_to_dict(self):
        question = Question.objects.all()[1]
        data = question.flatten()
        self.assertEquals(len(data),1)
        
        
        


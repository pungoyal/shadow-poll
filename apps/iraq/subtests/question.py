import unittest
import rapidsms
from iraq.models import *

class QuestionTest(unittest.TestCase):
    fixtures= ['question.json']
    def test_to_dict(self):
        question = Question.objects.all()[0]
        data = question.flatten()
        self.assertEquals(len(data),1)
        
        
        


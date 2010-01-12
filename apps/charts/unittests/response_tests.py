import unittest
import rapidsms
from rapidsms.tests.scripted import TestScript
from charts.models import Responses

class ResponseTests (unittest.TestCase):
    def test_load_all_answers_to_first_question(self):
        noOfAnswers = Responses().number_of_answers()
        self.assertEquals(noOfAnswers,5)
    

import unittest
import rapidsms
from rapidsms.tests.scripted import TestScript
from charts.models import Responses

class ResponseTests (unittest.TestCase):
    def testLoadAllAnswersToTheFirstQuestion(self):
        noOfAnswers = Responses().number_of_answers()
        self.assertEquals(noOfAnswers,5)

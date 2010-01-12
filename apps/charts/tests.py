import unittest
import rapidsms
from rapidsms.tests.scripted import TestScript
from app import App
from models import Responses

class TestApp (unittest.TestCase):
    def testLoadAllAnswersToTheFirstQuestion(self):
        noOfAnswers = Responses().numberOfAnswers()
        self.assertEquals(noOfAnswers,1)

        
        

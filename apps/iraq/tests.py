import unittest
import rapidsms
from models import *
from rapidsms.tests.scripted import TestScript
from app import App

class ResponderTest(unittest.TestCase):
    def testParseForChoiceAgeAndGender(self):
        poll_response = PollResponse(mobile_number = 1000)
        response = poll_response.generateResponse("ED 16 F")

        self.assertEquals(poll_response.age, '16')
        self.assertEquals(poll_response.gender,'F')
        self.assertEquals(response, "Thanks for participating. You selected Education.")

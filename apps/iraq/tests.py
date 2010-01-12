import unittest
import rapidsms
from models import *
from rapidsms.tests.scripted import TestScript
from app import App

class ResponderTest(unittest.TestCase):
    def setUp(self):
        self.poll_response = PollResponse(mobile_number = 1000)

    def testParseResponse(self):
        response = self.poll_response.generateResponse("ED 16 F 110001")

        self.assertEquals(self.poll_response.age, '16')
        self.assertEquals(self.poll_response.gender,'F')
        self.assertEquals(self.poll_response.location,"110001")
        self.assertEquals(response, "Thanks for participating. You selected Education.")
    def _testLocationIsOptional(self):
        response = self.poll_response.generateResponse("ED 12 M")

        self.assertEquals(self.poll_response.age, '12')
        self.assertEquals(self.poll_response.gender,'M')
        self.assertEquals(self.poll_response.location,None)
        self.assertEquals(response, "Thanks for participating. You selected Education.")

    def _testErrorScenarios(self):
        response = self.poll_response.generateResponse("EV")
        response = self.poll_response.generateResponse("ED 12")
        response = self.poll_response.generateResponse("ED")
        response = self.poll_response.generateResponse("EV")
        response = self.poll_response.generateResponse("ED 12 F 110001 Foo")
        response = self.poll_response.generateResponse("ED M 12 110001")

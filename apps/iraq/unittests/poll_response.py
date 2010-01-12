import unittest
import rapidsms
from iraq.models import *
from rapidsms.tests.scripted import TestScript
from iraq.app import App

class PollResponseTest(unittest.TestCase):
    def setUp(self):
        self.poll_response = PollResponse(mobile_number = 1000)

    def testParseResponse(self):
        response = self.poll_response.generate_response("ED 16 F 110001")

        self.assertEquals(self.poll_response.age, '16')
        self.assertEquals(self.poll_response.gender,'F')
        self.assertEquals(self.poll_response.location,"110001")
        self.assertEquals(response, "Thank you for voting. You selected Education as your number one issue.")
        
    def testLocationIsOptional(self):
        response = self.poll_response.generate_response("ED 12 M")

        self.assertEquals(self.poll_response.age, '12')
        self.assertEquals(self.poll_response.gender,'M')
        self.assertEquals(self.poll_response.location, None)
        self.assertEquals(response, "Thank you for voting. You selected Education as your number one issue.")

    def testExtraInfoInTheMessageIsIgnored(self):
        response = self.poll_response.generate_response("ED 16 F 110001 Foo Bar")

        self.assertEquals(self.poll_response.age, '16')
        self.assertEquals(self.poll_response.gender,'F')
        self.assertEquals(self.poll_response.location,"110001")
        self.assertEquals(response, "Thank you for voting. You selected Education as your number one issue.")        

    def testIncorrectResponseMessageOnBadParsing(self):
        error_message = "Sorry, we did not understand your response. Please re-send as - issue age gender area"

        response = self.poll_response.generate_response("ED M 12 110001")
        self.assertEquals(response, error_message)
        response = self.poll_response.generate_response("EV")
        self.assertEquals(response, error_message)
        response = self.poll_response.generate_response("ED 12")
        self.assertEquals(response, error_message)
        response = self.poll_response.generate_response("ED")
        self.assertEquals(response, error_message)

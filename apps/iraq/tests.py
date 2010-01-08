import unittest
import rapidsms
from models import *
from rapidsms.tests.scripted import TestScript
from app import App

class ResponderTest(unittest.TestCase):
    def testParseForChoiceAgeAndGender(self):
        poll_response = PollResponse()
        response = poll_response.generateResponse("ED;16;F",1000)
        self.assertEquals(poll_response.age, '16')
        self.assertEquals(poll_response.gender,'F')
        self.assertEquals(response, "Thanks for participating. You selected Education.")

class TestApp (TestScript):
    apps = (App,)

    # define your test scripts here.
    # e.g.:
    #
    # testRegister = """
    #   8005551212 > register as someuser
    #   8005551212 < Registered new user 'someuser' for 8005551212!
    #   8005551212 > tell anotheruser what's up??
    #   8005550000 < someuser said "what's up??"
    # """
    #
    # You can also do normal unittest.TestCase methods:
    #
    # def testMyModel (self):
    #   self.assertEquals(...)

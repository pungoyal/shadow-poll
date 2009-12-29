import unittest
from django.test.client import Client
from polls.models import Choice

class ChoiceTest(unittest.TestCase):
    def setUp(self):
        self.firstChoice = Choice.objects.create(poll_id=0, choice="option_one", votes=5)

    def testUnicode(self):
        self.assertEquals(str(self.firstChoice), 'option_one:5')

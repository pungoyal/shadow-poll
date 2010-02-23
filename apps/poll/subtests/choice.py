from apps.poll.models import *
from unittest import TestCase

class ChoiceTest(TestCase):

    def test_parse(self):
        question = Question(text = 'question 1', max_choices = 3)
        question.save()

        choice = Choice(code='a',question = question)
        choice.save()
  
        self.assertFalse(choice.parse("wefhjk"))
        self.assertTrue(choice.parse("a"))
        self.assertFalse(choice.parse(None))

    def test_unicode(self):
        c = Choice(code="b", text="text")
        self.assertEquals(str(c), "text:b")
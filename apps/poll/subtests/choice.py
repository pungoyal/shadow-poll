from apps.poll.models import *
from unittest import TestCase

class ChoiceTest(TestCase):
    
    def setUp(self):
        self.question = Question(text = 'question 1', max_choices = 3)
        self.question.save()
        
        self.category = Category(name="Dummy")
        self.category.save()
        self.choice = Choice(code='a',question = self.question, category = self.category)
        self.choice.save()

    def test_parse(self):
        self.assertFalse(self.choice.parse("wefhjk"))
        self.assertTrue(self.choice.parse("a"))
        self.assertFalse(self.choice.parse(None))

    def test_category(self):
        self.assertEquals(self.choice.category, self.category)

    def test_unicode(self):
        c = Choice(code="b", text="text")
        self.assertEquals(str(c), "text:b")

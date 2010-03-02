from apps.poll.models import *
from unittest import TestCase
from poll.models import Color

class ChoiceTest(TestCase):
    
    def setUp(self):
        Question.objects.all().delete()
        self.question = Question(text = 'question 1', max_choices = 3)
        self.question.save()

        self.color = Color(name = "pink", file_name = "pink.jpg")
        self.color.save()
        self.category = Category(name="Dummy", color = self.color)
        self.category.save()
        
        self.choice = Choice(code='a',question = self.question, category = self.category)
        self.choice.save()

    def test_parse(self):
        self.assertFalse(self.choice.parse("wefhjk"))
        self.assertTrue(self.choice.parse("a"))
        self.assertFalse(self.choice.parse(None))

    def test_category(self):
        self.assertEquals(self.choice.category, self.category)
        self.assertEquals(self.category.color, self.color)

    def test_unicode(self):
        c = Choice(code="b", text="text")
        self.assertEquals(str(c), "text:b")

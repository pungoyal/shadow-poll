from django.test import TestCase
import rapidsms
from iraq.models import *

class QuestionTest(TestCase):
    fixtures = ['question']
    def test_flatten_just_question(self):
        question = Question.objects.all()[2]
        data = question.flatten()
        self.assertEquals(len(data),3)
        self.assertTrue(self.is_not_empty(data[0]))
        self.assertTrue(self.is_empty(data[1]))
        self.assertTrue(self.is_empty(data[2]))
        
    def test_flatten_question_with_two_choices(self):
        question = Question.objects.all()[1]
        data = question.flatten()
        self.assertEquals(len(data),3)
        self.assertTrue(self.is_not_empty(data[0]))
        self.assertTrue(self.is_not_empty(data[1]))
        self.assertTrue(self.is_empty(data[2]))

    def test_flatten_question_fully_loaded(self):
        question = Question.objects.all()[0]
        data = question.flatten()
        self.assertEquals(len(data),3)
        self.assertTrue(self.is_not_empty(data[0]))
        self.assertTrue(self.is_not_empty(data[1]))
        self.assertTrue(self.is_not_empty(data[2]))

    def is_empty(self, li):
        return len(li) < 1

    def is_not_empty(self, li):
        return len(li) > 0

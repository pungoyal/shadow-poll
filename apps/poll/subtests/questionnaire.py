from apps.poll.models import *
from django.test import TestCase

class QuestionnaireTest(TestCase):
    def test_first_question(self):
        questionnaire = Questionnaire.objects.get(id=1)
        first_question = questionnaire.first_question()

        self.assertEquals(first_question.id, 1)

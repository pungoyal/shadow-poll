from django.test import TestCase
import rapidsms
from poll.models import *

class QuestionTest(TestCase):
    fixtures = ['question']
    def is_empty(self, li):
        return len(li) < 1

    def is_not_empty(self, li):
        return len(li) > 0

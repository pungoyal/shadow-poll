from rapidsms.tests.scripted import TestScript
from poll.app import App as poll_App
import reporters.app as reporters_app
import internationalization.app as i18n_app
from poll.models import *
from reporters.models import Reporter, PersistantConnection, PersistantBackend
import unittest

class ChoiceTest(TestScript):
    apps = (poll_App,)

    def test_parse(self):
        question = Question(text = 'question 1', max_choices = 3)
        question.save()
        c1 = Choice(code='a',question = question)
        c1.save()
  
        self.assertFalse(c1.parse("wefhjk"))
        self.assertTrue(c1.parse("a"))
        self.assertFalse(c1.parse(None))
        


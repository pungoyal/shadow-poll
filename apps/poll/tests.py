from rapidsms.tests.scripted import TestScript
from app import App
import reporters.app as reporters_app
import internationalization.app as i18n_app

from models import *
from reporters.models import Reporter, PersistantConnection, PersistantBackend
import unittest

class QuestionTreeTest(TestScript):
    apps = (App,)

    def testNext(self):
        question1 = Question(text = 'question 1')
        question2 = Question(text = 'question 2')
        
        tree = QuestionTree()
        tree.addQuestion(question1)
        tree.addQuestion(question2)
        
        nextquestion = tree.next(question1)
        self.assertEquals(nextquestion, question2)    
        

from rapidsms.tests.scripted import TestScript
from poll.app import App as poll_App
import reporters.app as reporters_app
import internationalization.app as i18n_app
from poll.models import *
from reporters.models import Reporter, PersistantConnection, PersistantBackend
import unittest

class QuestionTreeTest(TestScript):
    apps = (poll_App,)

    def testNext(self):
        question1 = Question(text = 'question 1')
        question2 = Question(text = 'question 2')
        
        tree = Questionnaire()
        tree.addQuestion(question1)
        tree.addQuestion(question2)
        
        nextquestion = tree.next(question1)
        self.assertEquals(nextquestion, question2)    
        
    def testLastQuestion(self):
        question1 = Question(text = 'question 1')
        
        self.tree = Questionnaire()
        self.tree.addQuestion(question1)
        
        nextquestion = self.tree.next(question1)
        self.assertEquals(nextquestion, None)    
    
    def testFirst(self):
        question1 = Question(text = 'question 1')
        
        self.tree = Questionnaire()
        self.tree.addQuestion(question1)
        
        nextquestion = self.tree.first()
        self.assertEquals(nextquestion, question1)    
    
    def testCurrentTree(self):
        question1 = Question(text = 'question 1')
        
        self.tree = Questionnaire()
        self.tree.addQuestion(question1)
        self.tree.save()
        current  = Questionnaire.load_current()
        self.assertEquals(self.tree, current)

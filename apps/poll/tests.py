from django.test import TestCase
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
        
    def testLastQuestion(self):
        question1 = Question(text = 'question 1')
        
        self.tree = QuestionTree()
        self.tree.addQuestion(question1)
        
        nextquestion = self.tree.next(question1)
        self.assertEquals(nextquestion, None)    
    
    def testFirst(self):
        question1 = Question(text = 'question 1')
        
        self.tree = QuestionTree()
        self.tree.addQuestion(question1)
        
        nextquestion = self.tree.first()
        self.assertEquals(nextquestion, question1)    
    
    def testCurrentTree(self):
        question1 = Question(text = 'question 1')
        
        self.tree = QuestionTree()
        self.tree.addQuestion(question1)
        self.tree.save()
        current  = QuestionTree.load_current()
        self.assertEquals(self.tree, current)

class UserSessionTest(TestCase):
    apps = (App,)

    def setUp(self):
        self.backend = PersistantBackend(slug="MockBackend")
        self.backend.save()
        self.reporter = Reporter(alias="ReporterName")
        self.reporter.save()
        self.pconnection = PersistantConnection(backend=self.backend, 
                                                reporter=self.reporter, 
                                                identity="1000")
        self.pconnection.save()
        self.reporter.connections.add(self.pconnection)
        
        self.tree = QuestionTree()
        self.question1 = Question("question1")
        self.question2 = Question("question2")
        self.question3 = Question("question3")
        self.tree.addQuestion(self.question1)
        self.tree.addQuestion(self.question2)
        self.tree.addQuestion(self.question3)
        self.tree.save()

    def testOpenNewSession(self):
        self.session = UserSession.open(self.pconnection)
        self.assertEquals(self.session.tree, self.tree)
        self.assertEquals(self.session.question, None)
        


from rapidsms.tests.scripted import TestScript
from poll.app import App as poll_App
import reporters.app as reporters_app
import internationalization.app as i18n_app
from poll.models import *
from reporters.models import Reporter, PersistantConnection, PersistantBackend
import unittest

class QuestionTest(TestScript):
    apps = (poll_App,)

    def test_save(self):
        initial_no_of_questions = len(Question.objects.all())
        question1 = Question(text = 'question 1', max_choices = 3)
        question2 = Question(text = 'question 2', max_choices = 3)
        
        question1.next_question = question2
        question1.save()
        question2.save()
        

    def test_last_question(self):
        question1 = Question(text = 'question 1')
        question1.save()
        next_question = question1.next_question
        self.assertEquals(next_question, None)    
    
    def test_first(self):
        question1 = Question(text = 'question 1')
        question2 = Question(text = 'question 2')
        question3 = Question(text = 'question 3')
        
        question2.is_first = True
      
        question1.save()
        question2.save()
        question3.save()

        first_question = Question.first()
        
        self.assertEquals(first_question, question2)    
    

    def setup_choices(self,question):
        choice1 = Choice(code= 'a',question=question)
        choice2 = Choice(code= 'b',question=question)
        choice3 = Choice(code= 'c',question=question)
        choice1.save()
        choice2.save()
        choice3.save()

    def test_matching_choices(self):
        question1 = Question(text = 'question 1',max_choices = 1)
        question1.save()
        self.setup_choices(question1)
        self.assertEquals(len(question1.matching_choices('jdenjn')), 0)
        self.assertEquals(len(question1.matching_choices('a')), 1)
        self.assertEquals(len(question1.matching_choices(None)), 0)
       

from django.db import models
from apps.reporters.models import Reporter, PersistantConnection
import re
from register.models import Registration

class QuestionTree(models.Model):

    def __init__(self):
        self.questions = []
        self.flow = {}

    def addQuestion(self, question):
        self.addToTheFlow(question)
        self.questions.append(question)

    def addToTheFlow(self, question):
        if len(self.questions) == 0 :  
            self.flow[question] = None
            return
 
        self.flow[self.questions[-1]] =question

    def next(self, question):
         return self.flow[question]
    
    def first(self):
        return self.flow.keys()[0]


class Question(models.Model):
    text = models.TextField()
    max_choices = models.IntegerField()
    error_response = models.TextField(null=True, blank=True)
    question_tree = models.ForeignKey(QuestionTree) 
    
    def __unicode__(self):
        return "Q%s: %s" % (
            self.pk,
            self.text)
    
class Choice(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    


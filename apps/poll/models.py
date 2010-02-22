from django.db import models
from apps.reporters.models import Reporter, PersistantConnection
import re
from register.models import Registration

class Questionnaire(models.Model):
    name = models.TextField(null=True)

    def __init__(self, *args, **kargs):
        super(Questionnaire, self).__init__(*args,**kargs)
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

    @classmethod
    def load_current(klass):
        return Questionnaire.objects.all()[0]


class Question(models.Model):
    text = models.TextField()
    max_choices = models.IntegerField()
    error_response = models.TextField(null=True, blank=True)
    question_tree = models.ForeignKey(Questionnaire) 
    
    def __unicode__(self):
        return "Q%s: %s" % (
            self.pk,
            self.text)

class UserSession(models.Model):
    connection = models.ForeignKey(PersistantConnection)
    questionnaire = models.ForeignKey(Questionnaire)
    question = models.ForeignKey(Question, null=True)

    @classmethod
    def open(klass,connection):
        sessions = UserSession.objects.filter(connection = connection)
        if len(sessions) == 0:
            session = UserSession()
            session.connection = connection
            session.questionnaire = Questionnaire.load_current()
            session.question = None
            return session
        return None
        

class Choice(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    


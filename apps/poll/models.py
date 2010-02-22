from django.db import models
from apps.reporters.models import Reporter, PersistantConnection
import re
from register.models import Registration

class Question(models.Model):
    text = models.TextField()
    max_choices = models.IntegerField(default=3)
    error_response = models.TextField(null=True, blank=True)
    next_question = models.ForeignKey('self', null=True)
    is_first = models.BooleanField(default=False)

    def __unicode__(self):
        return " %s" % (self.text)

    def respond(self,answer):
        all_choices = Choice.objects.filter(question = self)
        for choice in all_choices:
            if choice.parse(answer):
                return True
        return False
        
    @classmethod
    def first(klass):
        return Question.objects.filter(is_first=True)[0]

        

class Choice(models.Model):
    code = models.CharField(max_length=1)
    text = models.TextField(null=True)
    question = models.ForeignKey(Question)
    
    def parse(self, response):
        return self.code == response
        

class UserSession(models.Model):
    connection = models.ForeignKey(PersistantConnection)
    question = models.ForeignKey(Question, null=True)
        
    def respond(self, message):
        if self._first_access():
            self.question = Question.first()
            return self.question.text
            
        if self.question.respond(message):
            self.question = self.question.next_question
            return self.question.text   
        
        return "error_parsing_response"
    
    def _first_access(self):
        return self.question == None


    @classmethod
    def open(klass,connection):
        sessions = UserSession.objects.filter(connection = connection)
        if len(sessions) == 0:
            session = UserSession()
            session.connection = connection
            session.question = None
            return session
        return None

from django.db import models
from apps.reporters.models import Reporter, PersistantConnection
import re
from register.models import Registration

#only one questionnaire object in the db to hold the trigger for the poll
class Questionnaire(models.Model):
    trigger = models.CharField(max_length=10)
    
    def __unicode__(self):
        return "%s" % (self.trigger)


class Question(models.Model):
    text = models.TextField()
    max_choices = models.IntegerField(default=3)
    error_response = models.TextField(null=True, blank=True)
    next_question = models.ForeignKey('self', null = True,default = None)
    is_first = models.BooleanField(default=False)

    def __unicode__(self):
        return " %s" % (self.text)

    def matching_choices(self,answer):
        matching_choices = []
        all_choices = Choice.objects.filter(question = self)
        for choice in all_choices:
            if choice.parse(answer):
                matching_choices.append(choice)
        return matching_choices
        

    @classmethod
    def first(klass):
        return Question.objects.filter(is_first=True)[0]

class Choice(models.Model):
    code = models.CharField(max_length=2)
    text = models.TextField(null=True)
    question = models.ForeignKey(Question)
    
    def parse(self, response):
        return self.code == response
        

class User(models.Model):
    connection = models.ForeignKey(PersistantConnection)


class UserSession(models.Model):
    user = models.ForeignKey(User, null=True)
    connection = models.ForeignKey(PersistantConnection)
    question = models.ForeignKey(Question, null=True)
    
    def respond(self, message):
        if self._is_trigger(message):
            self.question = None

        if self._first_access():
            self.question = Question.first()
            self.save()
            self._save_user()
            return self.question.text
           
        matching_choices = self.question.matching_choices(message)
        if len(matching_choices) > 0:
            self._save_response(self.question, matching_choices)
            self.question = self.question.next_question
            return self._next_question(self.question)   
        
        self.save()
        return "error_parsing_response"
    
    def _save_response(self,question,choices):
        for choice in choices:
            user_response = UserResponse(user = self.user, question =question, choice = choice)
            user_response.save()

    def _save_user(self):
        self.user = User(connection = self.connection)
        self.user.save()
    
    def _next_question(self,question):
        if question == None:
            return "thanks"
        return question.text
        
    

    def _first_access(self):
        return self.question == None

    def _is_trigger(self, message):
        for questionnaire in Questionnaire.objects.all():
            if message.startswith(questionnaire.trigger):
                return True
        return False

    # assuming only one session for a connection throughout the poll
    @classmethod
    def open(klass,connection):
        sessions = UserSession.objects.filter(connection = connection)
        if len(sessions) == 0:
            session = UserSession()
            session.connection = connection
            session.question = None
            return session
        return sessions[0]
    
    
class UserResponse(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice)
    


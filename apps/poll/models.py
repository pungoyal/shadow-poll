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
        return "Q%s: %s" % (
            self.pk,
            self.text)
    @classmethod
    def first(klass):
        return Question.objects.filter(is_first=True)[0]


class Choice(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    

class UserSession(models.Model):
    connection = models.ForeignKey(PersistantConnection)
    question = models.ForeignKey(Question, null=True)

    @classmethod
    def open(klass,connection):
        sessions = UserSession.objects.filter(connection = connection)
        if len(sessions) == 0:
            session = UserSession()
            session.connection = connection
            session.question = Question.first()
            return session
        return None
        
    def respond(self, message):
        return Question.first().text



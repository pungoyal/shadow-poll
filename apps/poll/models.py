from __future__ import division
import re
from django.db import models
from apps.reporters.models import Reporter, PersistantConnection
from apps.register.models import Registration
from django.db.models import Avg,Count
import math

"""
'Separator' is what differentiates arguments in the messages we accept.
This will most probably be a space, but we pull it out here on the off-chance
that this ends up being something else (like a semi-colon)
"""
SEPARATOR = ' '

#only one questionnaire object in the db to hold the trigger for the poll
class Questionnaire(models.Model):
# users can launch a poll by texting 'trigger param param'
# where 'param' is any one of the demographic data which
# links to questionnaire
    trigger = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s" % (self.trigger)

DATA_TYPE = ( ('i','integer'), ('s','string'), ('c','character') )
class DemographicData(models.Model):
    """ This is a db model so that we can add an arbitrary number
    of demographic data to any given poll"""
    questionnaire = models.ForeignKey(Questionnaire)
    name = models.CharField(max_length=32)
    regex = models.CharField(max_length=32)
    order = models.IntegerField()
    type = models.CharField(max_length=16, choices=DATA_TYPE)

class Question(models.Model):
    text = models.TextField()
    max_choices = models.IntegerField(default=1)
    helper_text = models.CharField(max_length=100, default='')
    error_response = models.TextField(null=True, blank=True)
    next_question = models.ForeignKey('self', null = True,default = None)
    is_first = models.BooleanField(default=False)

    def __unicode__(self):
        options = self.humanize_options()
        return "%s %s %s" % (self.text,self.helper_text, options)

    def response_break_up(self):
        break_up = []
        relevant_responses = UserResponse.objects.filter(question=self)

        grouped_responses = relevant_responses.values('choice').annotate(Count('choice'))
        total_responses = relevant_responses.aggregate(Count('choice'))

        for gr in grouped_responses:
            break_up.append(round(gr['choice__count']*100/total_responses['choice__count'], 1))

        return break_up


    def humanize_options(self):
        choices = Choice.objects.filter(question=self)
        text = []
        for ch in choices:
            text.append(ch.code + ". "+ch.text)

        return " ".join(text)

    def matching_choices(self,answer):
        matching_choices = []
        if answer == None:
            return matching_choices

        all_choices = Choice.objects.filter(question = self)
        answered_choices = answer.strip(' ').rsplit(' ')

        for answered_choice in answered_choices:
            for choice in all_choices:
                if choice.parse(answered_choice):
                    matching_choices.append(choice)
                    break

        return matching_choices if len(matching_choices) == len(answered_choices) else []

    @classmethod
    def first(klass):
        firsts= Question.objects.filter(is_first=True)
        return firsts[0] if len(firsts)>0 else None


class Choice(models.Model):
    code = models.CharField(max_length=2)
    text = models.TextField(null=True)
    question = models.ForeignKey(Question)

    def parse(self, response):
        return self.code == response

    def __unicode__(self):
        return "%s:%s" % (self.text, self.code)

GENDER = ( ('M', 'Male'), ('F', 'Female') )

class User(models.Model):
    connection = models.ForeignKey(PersistantConnection, null=True)
    age = models.IntegerField(default=None, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, default=None, 
                              null=True, blank=True)
    location = models.IntegerField(null=True)

    def __unicode__(self):
        return " User : connection %s" % str(self.connection)


class UserSession(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question, null=True)
    questionnaire = models.ForeignKey(Questionnaire, null=True)
    
    def __unicode__(self):
        return "session for : %s" % (self.user)

    def respond(self, message):
        if self._is_trigger(message):
            self.question = None

        if self._first_access():
            self.question = Question.first()

            temp_user = self.user
            temp_user.save()
            self.user = temp_user

            self.save()
            return str(self.question)


        matching_choices = self.question.matching_choices(message)

        if len(matching_choices) > 0:
            self._save_response(self.question, matching_choices)
            self.question = self.question.next_question
            self.save()
            return self._next_question(self.question)   

        self.save()
        return "error_parsing_response"

    def _save_response(self,question,choices):
        for choice in choices:
            user_response = UserResponse(user = self.user, question =question, choice = choice)
            user_response.save()

    def _next_question(self,question):
        if question == None:
            return "thanks"
        return str(question)

    def _first_access(self):
        return self.question == None

    def _is_trigger(self, message):
        for questionnaire in Questionnaire.objects.all():
            if message.strip().lower().startswith(questionnaire.trigger.strip().lower()):
                self.questionnaire = questionnaire
                return True
        return False

    # assuming only one session for a connection throughout the poll
    @classmethod
    def open(klass,connection):
        users = User.objects.filter(connection = connection)
        temp_user = users[0] if(len(users)) > 0 else User(connection = connection)
        sessions = UserSession.objects.filter(user = temp_user)
        if len(sessions) == 0:
            session = UserSession(question = None)
            session.user = temp_user
            return session

        return sessions[0]

class UserResponse(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice)    

from __future__ import division
import re
from django.db import models
from apps.reporters.models import Reporter, PersistantConnection
from apps.register.models import Registration
from django.db.models import Avg,Count
import math

##########################################################################

SEPARATOR = ' '
DATA_TYPE = ( ('i','integer'), ('s','string'), ('c','character') )
GENDER = ( ('M', 'Male'), ('F', 'Female') )

##########################################################################

#only one questionnaire object in the db to hold the trigger for the poll
class Questionnaire(models.Model):
    trigger = models.CharField(max_length=10)
    max_retries = models.IntegerField(null=True)

    def __unicode__(self):
        return "%s" % (self.trigger)

##########################################################################

class DemographicParser(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    name = models.CharField(max_length=32)
    regex = models.CharField(max_length=32)
    order = models.IntegerField()
    type = models.CharField(max_length=16, choices=DATA_TYPE)

    def parse_and_set(self, message, user) :
        arguments = message.split(SEPARATOR)
        for a in arguments:
            regex = re.compile( '(%s)$' % self.regex.strip().lower() )
            match = regex.match( a )
            if match:
                if self.type == 'i':
                    val = int(match.group(0))
                elif self.type == 'c':
                    val = match.group(0)[0]
                else:
                    val = match.group(0)
                if hasattr(user, self.name):
                        setattr(user, self.name, val)
                        break

##########################################################################

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

    def most_voted_category_by_governorate(self, governorate_id):
        relevant_responses = UserResponse.objects.filter(user__governorate = governorate_id)
        
        if len(relevant_responses) < 1 :
            return None
        
        choice_id =  relevant_responses.values('choice').annotate(Count('choice')).order_by('-choice__count')[0]['choice']
        return Category.objects.get(choice__id = choice_id)

    def get_number_of_responses_by_governorate(self, governorate_id):
        return len(UserResponse.objects.filter(user__governorate = governorate_id))

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

##########################################################################
class Color(models.Model):
    name = models.CharField(max_length=10)
    file_name = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.name

##########################################################################

class Category(models.Model):
    name = models.CharField(max_length=25)
    color = models.ForeignKey(Color)
    
    def __unicode__(self):
        return self.name

##########################################################################
class Choice(models.Model):
    code = models.CharField(max_length=2)
    text = models.TextField(null=True)
    question = models.ForeignKey(Question)
    category = models.ForeignKey(Category, null = True)

    def parse(self, response):
        return self.code == response

    def __unicode__(self):
        return "%s:%s" % (self.text, self.code)

##########################################################################

class User(models.Model):
    connection = models.ForeignKey(PersistantConnection, null=True)
    age = models.IntegerField(default=None, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, default=None, 
                              null=True, blank=True)
    governorate = models.IntegerField(null=True)
    district = models.IntegerField(null=True)

    def __unicode__(self):
        return " User : connection %s" % str(self.connection)

##########################################################################

class UserSession(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question, null=True)
    questionnaire = models.ForeignKey(Questionnaire, null=True)
    num_attempt = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "session for : %s" % (self.user)

    def respond(self, message):

        if self._is_trigger(message):
            self.question = None
            self.user = self._save_user(self.user, message)

        if self._first_access():
            self.question = Question.first()
            self.save()
            return str(self.question)


        matching_choices = self.question.matching_choices(message)
        
        if len(matching_choices) > 0:
            self._save_response(self.question, matching_choices)
            self.question = self.question.next_question
            self.num_attempt = 1
            self.save()
            return self._next_question(self.question)
        
        if self._has_user_exceeded_max_attempts():
            self.question = None
            self.num_attempt = 1
            self.save()
            return "err3"
        
        self.num_attempt = self.num_attempt + 1
        self.save()
        return "error_parsing_response"

    def _save_user(self, user, message):
        message = message.strip().lstrip(self.questionnaire.trigger.lower()).strip()
        parsers = list( DemographicParser.objects.filter(questionnaire=self.questionnaire).order_by('order') )
        for parser in parsers:
            parser.parse_and_set(message, user)
        user.save()
        return user

 
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
    
    def _has_user_exceeded_max_attempts(self):
        max_r = Questionnaire.objects.all()[0].max_retries
        return self.num_attempt >= max_r

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

##########################################################################

class UserResponse(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice)    

##########################################################################

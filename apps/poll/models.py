from __future__ import division
import re
import math
from datetime import datetime
from django.db import models
from django.db.models import Avg,Count
from django.db.models import Q
from apps.internationalization.utils import get_translation as _
from apps.poll.messages import *
from apps.poll.string import clean, has_word
from apps.poll.list import remove_duplicates
from apps.reporters.models import Reporter, PersistantConnection
##########################################################################

SEPARATOR = ' '
DATA_TYPE = ( ('i','integer'), ('s','string'), ('c','character') )
# the male and female option should be lower case, to facilitate
# mapping login in demographic parser
GENDER = ( ('m', 'Male'), ('f', 'Female') )


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
    mandatory = models.BooleanField()

    def __unicode__(self):
        return "%s" % (self.name)

    def parse(self, message) :
        arguments = message.split(SEPARATOR)
        val = None
        for a in arguments:
            regex = re.compile( '(%s)$' % str(self.regex).strip() )
            match = regex.match( a.lower() )
            if match:
                if self.type == 'i':
                    val = int(match.group(0))
                elif self.type == 'c':
                    val = match.group(0)[0]
                else:
                    val = match.group(0)
                break     
        return val

##########################################################################

class Question(models.Model):
    text = models.TextField()
    num_answers_expected = models.IntegerField(default=1)
    helper_text = models.CharField(max_length=100, default='')
    error_response = models.TextField(null=True, blank=True)
    next_question = models.ForeignKey('self', null = True,default = None)
    is_first = models.BooleanField(default=False)

    def __unicode__(self):
        options = self.humanize_options()
        return "%s: %s %s" % (self.text,self.helper_text, options)

    def response_break_up(self, governorate_code=None, district_code = None, gender=None, age_group=None):
        relevant_responses = UserResponse.objects.filter(question=self)
        if governorate_code != None:
            relevant_responses = relevant_responses.filter(user__governorate=governorate_code)
        if district_code != None:
            relevant_responses = relevant_responses.filter(user__district = district_code)
        if gender != None:
            relevant_responses = relevant_responses.filter(user__gender=gender)
        if age_group != None and len(age_group) == 2 :
            relevant_responses = relevant_responses.filter(Q(user__age__gt = age_group[0]) | Q(user__age = age_group[0])  , Q(user__age = age_group[0]) | Q( user__age__lt = age_group[1]))
        responses_by_choice = relevant_responses.values("choice").\
            annotate(votes = Count("choice"))
        responses_by_category = relevant_responses.values("choice__category").\
            annotate(votes = Count("choice__category")).order_by("-votes")
        return { "by_choice": responses_by_choice, "by_category" :responses_by_category }

    def get_categories(self):
        category_set = set( choice.category for choice in Choice.objects.filter(question=self) )
        return list(category_set)

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
        answered_choices = remove_duplicates(answer.strip(' ').rsplit(' '))
        
        for answered_choice in answered_choices:
            for choice in all_choices:
                if choice.parse(answered_choice) :
                    matching_choices.append(choice) 
                    break

        return matching_choices if len(matching_choices) == len(answered_choices) else []

    @classmethod
    def first(klass):
        firsts= Question.objects.filter(is_first=True)
        return firsts[0] if len(firsts)>0 else None

##########################################################################
class Color(models.Model):
    """ ro - color has nothing to do with poll. This should be in charts app."""
    file_name = models.CharField(max_length=20)
    code = models.CharField(max_length=25)

    def __unicode__(self):
        return "file:%s code:%s" % (self.file_name, self.code)

##########################################################################

class Category(models.Model):
    name = models.CharField(max_length=25)
    color = models.ForeignKey(Color)
    
    def __unicode__(self):
        return self.name

    @staticmethod
    def most_popular(user_responses):
        """ user_responses is a django query object """
        if len(user_responses) < 1 :
            return None
        category_id =  user_responses.values('choice__category')\
                       .annotate(Count('choice__category'))\
                       .order_by('-choice__category__count', 'choice__category')\
                       [0]['choice__category']
        return Category.objects.get(pk = category_id)    

##########################################################################
class Choice(models.Model):
    code = models.CharField(max_length=2)
    text = models.TextField(null=True)
    question = models.ForeignKey(Question)
    category = models.ForeignKey(Category, null = True)

    def __unicode__(self):
        return "%s:%s" % (self.text, self.code)
        
    def parse(self, response):
        return self.code == response

##########################################################################

class User(models.Model):
    connection = models.ForeignKey(PersistantConnection, null=True)
    age = models.IntegerField(default=None, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, default=None, 
                              null=True, blank=True)
    governorate = models.IntegerField(null=True)
    district = models.IntegerField(null=True)
    time_created = models.DateTimeField(default=datetime.now)
    active = models.BooleanField()

    def __unicode__(self):
        signature = "user connection: %s " % str(self.connection)
        if self.age:
            signature = signature + " age: %s" % self.age
        if self.gender:
            signature = signature + " gender: %s" % self.gender            
        return signature

    def set_user_geolocation_if_registered(self, connection):
        self.governorate = connection.governorate
        self.district = connection.district

    def set_value(self, field, value):
        if hasattr(self, field):
            setattr(self, field, value)

##########################################################################

class UserSession(models.Model):
    user = models.ForeignKey(User, null = True)
    question = models.ForeignKey(Question, null=True)
    questionnaire = models.ForeignKey(Questionnaire, null=True)
    num_attempt = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "session for : %s" % (self.user)

    def respond(self, message):
        # respond() takes the message object, so that
        # when we start supporting intelligent feedback,
        # we can pass the error_code, text, and parameters
        # back through the message object
        self._set_default_questionnaire()

        ''' respond to a trigger message'''
        response = self._respond_to_trigger(message)
        if response != None: 
            self._save_session()
            return response
        
        '''if its not a trigger its an attempt'''
        self.num_attempt = self.num_attempt + 1
        ''' respond to an answer '''
        response =  self._respond_to_answer(message)
        if response != None: 
            error_message =  self._respond_to_exceeding_attempts()
            self._save_session()
            return response if not error_message else error_message
        
        '''if last question answered'''
        response = self._respond_to_last_answer()
        if response != None:
            self._save_session()
            self._close_session()
            return response

        self._save_session()
        return str(self.question)

    def _respond_to_last_answer(self):
        if self.question == None:
            return FINAL_APPRECIATION_MESSAGE

    def _save_session(self):
        self.user = self._save_user(self.user)
        self.save()

    ''' default to the first questionnaire'''
    def _set_default_questionnaire(self):
        if not self.questionnaire:
            self.questionnaire = Questionnaire.objects.all().order_by('pk')[0]

    def _respond_to_trigger(self, message):
        if not self._is_trigger(message.text): return 
        ''' create new user '''
        self.user = User(connection = self.user.connection, governorate = self.user.governorate, district = self.user.district, active = True)
        text = message.text.strip().lstrip(self.questionnaire.trigger.lower()).strip()
        parsers = list(DemographicParser.objects.filter(questionnaire=self.questionnaire).order_by('order') )
        
        for parser in parsers:
            demographic_information = parser.parse(text)
            if demographic_information == None:
                return TRIGGER_INCORRECT_MESSAGE
            self.user.set_value(parser.name, demographic_information)
     
        self.question = Question.first()
        self.num_attempt = 0
        return str(self.question)

    def _respond_to_answer(self, message):
        if not self.question : 
            return TRIGGER_INCORRECT_MESSAGE

        matching_choices = self.question.matching_choices(message.text)
        if len(matching_choices) > 0:
            if(len(matching_choices) < self.question.num_answers_expected):
                return "err_less_than_expected_choices"
            if(len(matching_choices) > self.question.num_answers_expected):
                return "err_more_than_expected_choices"
            self._save_response(self.question, matching_choices)
            self.question = self.question.next_question
            self.num_attempt = 0
        else:
            return "error_parsing_response"
        

    def _respond_to_exceeding_attempts(self):
        if self._has_user_exceeded_max_attempts():
            self.num_attempt = 0
            self._close_session()
            return "session_closed_due_to_max_retries"
    
    def _save_user(self, user):
        if not user : return
        user.save()
        return user

    def _save_response(self,question,choices):
        for choice in choices:
            user_response = UserResponse(user = self.user, question =question, choice = choice)
            user_response.save()

    def _next_question(self,question):
        if question == None:
           self. _close_session()
           return FINAL_APPRECIATION_MESSAGE
        return str(question)

    def _close_session(self):
        if self.user :
            self.user.active = False
            self.user = self._save_user(self.user)
        self.save()

    def _first_access(self):
        return self.question == None

    def _is_trigger(self, text):
        for questionnaire in Questionnaire.objects.all():
            if  has_word((text, questionnaire.trigger)):
                self.questionnaire = questionnaire
                return True
        return False
    
    def _has_user_exceeded_max_attempts(self):
        max_r = Questionnaire.objects.all()[0].max_retries
        return self.num_attempt >= max_r

    @classmethod
    def open(klass,connection):
        users = User.objects.filter(connection = connection, governorate = connection.governorate, district = connection.district, active = True).order_by('-time_created')
        user = users[0] if(len(users)) > 0 else User(connection = connection, governorate = connection.governorate, district = connection.district, active = True)
        sessions = UserSession.objects.filter(user = user)
        if len(sessions) == 0:
            session = UserSession(question = None)
            user.set_user_geolocation_if_registered(connection)
            session.user = user
            return session

        return sessions[0]


##########################################################################

class UserResponse(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice)    

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "USER: %s, QUESTION: %s, RESPONSE: %s" % (self.user.connection, self.question.pk, self.choice)

##########################################################################

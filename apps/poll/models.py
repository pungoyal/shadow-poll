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
# the male and female option should be lower case, to facilitate
# mapping login in demographic parser
GENDER = ( ('m', 'Male'), ('f', 'Female') )

FINAL_APPRECIATION_MESSAGE = 'thanks'
TRIGGER_INCORRECT_MESSAGE = 'trigger_error'

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

class ResponseBreakUp():
    #FAAFBE is the default color that shows up when there are no responses for a level
    def __init__(self, text="No responses yet", percentage=0, color="#FAAFBE"):
        self.text = text
        self.percentage = percentage
        self.color = color

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
        return "%s: %s %s" % (self.text,self.helper_text, options)

    def response_break_up(self, governorate_id=None):
        """ 
        returns the percentage of votes going to each category as a list
        if no responses are received yet, then return empty list
        """
        relevant_responses = UserResponse.objects.filter(question=self)
        if governorate_id is not None:
            relevant_responses = relevant_responses.filter(user__governorate=governorate_id)
        grouped_responses = relevant_responses.values('choice').annotate(Count('choice')).order_by('choice')

        break_up = []

        if len(grouped_responses) == 0:
            break_up.append(ResponseBreakUp(text="No responses yet", percentage = 0, color= "#FAAFBE"))
            return break_up

        total_responses = relevant_responses.aggregate(Count('choice'))

        for group in grouped_responses:
            color = Category.objects.get(choice=group['choice']).color.code
            choice_text = Choice.objects.get(id=group['choice']).text
            percentage = round(group['choice__count']*100/total_responses['choice__count'], 1)
            break_up.append(ResponseBreakUp(text=choice_text, percentage = percentage, color= color))
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
        choice_id =  user_responses.values('choice').annotate(Count('choice')).order_by('-choice__count')[0]['choice']
        return Category.objects.get(choice__id = choice_id)    

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

    def __unicode__(self):
        return "user connection : %s " % str(self.connection)

    def set_user_geolocation_if_registered(self, connection):
        self.governorate = connection.governorate
        self.district = connection.district

    def set_value(self, field, value):
        if hasattr(self, field):
            setattr(self, field, value)

##########################################################################

class UserSession(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question, null=True)
    questionnaire = models.ForeignKey(Questionnaire, null=True)
    num_attempt = models.IntegerField(default=1)
    
    def __unicode__(self):
        return "session for : %s" % (self.user)

    def respond(self, message):
        # default to the first questionnaire     
        if not self.questionnaire:
            self.questionnaire = Questionnaire.objects.all().order_by('pk')[0]

        if self._is_trigger(message):
            self.question = None
            message = message.strip().lstrip(self.questionnaire.trigger.lower()).strip()
            parsers = list(DemographicParser.objects.filter(questionnaire=self.questionnaire).order_by('order') )

            for parser in parsers:
                demographic_information = parser.parse(message)
                if demographic_information == None:
                    return TRIGGER_INCORRECT_MESSAGE
                self.user.set_value(parser.name, demographic_information)
                if not self.user_exist_with_same_demographic_info(self.user):
                    user = User(connection = self.user.connection, age = self.user.age, gender = self.user.gender, governorate = self.user.governorate, district = self.user.district)
                    self.user = user
                
            self.user = self._save_user(self.user)

        if self._first_access():
            if self.user.id == None:
                return TRIGGER_INCORRECT_MESSAGE
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
            return "session_closed_due_to_max_retries"
        
        self.num_attempt = self.num_attempt + 1
        self.save()
        return "error_parsing_response"

    def _save_user(self, user):
        user.save()
        return user

    def user_exist_with_same_demographic_info(self, user):
        users_with_same_demographic_info = User.objects.filter(connection = user.connection, age = user.age, gender = user.gender, governorate = user.governorate, district = user.district)
        if len(users_with_same_demographic_info) == 0:
            return False
        return True

    def _save_response(self,question,choices):
        for choice in choices:
            user_response = UserResponse(user = self.user, question =question, choice = choice)
            user_response.save()

    def _next_question(self,question):
        if question == None:
            return FINAL_APPRECIATION_MESSAGE
        return str(question)

    def _first_access(self):
        return self.question == None

    def _is_trigger(self, message):
        for questionnaire in Questionnaire.objects.all():
            if message.strip().lower().find(questionnaire.trigger.strip().lower()) > -1:
                self.questionnaire = questionnaire
                return True
        return False
    
    def _has_user_exceeded_max_attempts(self):
        max_r = Questionnaire.objects.all()[0].max_retries
        return self.num_attempt >= max_r

    @classmethod
    def open(klass,connection):
        users = User.objects.filter(connection = connection, governorate = connection.governorate, district = connection.district)
        user = users[0] if(len(users)) > 0 else User(connection = connection, governorate = connection.governorate, district = connection.district)
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

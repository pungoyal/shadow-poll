import re
from django.db import models
from apps.reporters.models import Reporter, PersistantConnection
from register.models import Registration

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
    error_response = models.TextField(null=True, blank=True)
    next_question = models.ForeignKey('self', null = True,default = None)
    is_first = models.BooleanField(default=False)

    def __unicode__(self):
        return " %s" % (self.text)

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
        # ro - this seems wrong. what happens when we have multiple questionnaires?
        return Question.objects.filter(is_first=True)[0]

class Choice(models.Model):
    code = models.CharField(max_length=2)
    text = models.TextField(null=True)
    question = models.ForeignKey(Question)
    
    def parse(self, response):
        return self.code == response
        
GENDER = ( ('M', 'Male'), ('F', 'Female') )
class User(models.Model):
    connection = models.ForeignKey(PersistantConnection)
    age = models.IntegerField(default=None, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, default=None, 
                              null=True, blank=True)

class UserSession(models.Model):
    user = models.ForeignKey(User, null=True)
    connection = models.ForeignKey(PersistantConnection)
    question = models.ForeignKey(Question, null=True)
    questionnaire = models.ForeignKey(Questionnaire, null=True)
    
    def respond(self, message):
        if self._is_trigger(message):
            self.question = None

        if self._first_access():
            self.question = Question.first()
            self.save()
            self._save_user(message)
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

    def _save_user(self, message):
        # todo : this could be made more generic to handle different kinds
        # of user registation criteria, similar to the forms app.
        self.user = User(connection = self.connection)
        message = message.strip().lstrip(self.questionnaire.trigger.lower()).strip()
        if len(message) != 0:
            # there are arguments
            arguments = message.split(SEPARATOR)
            data = list( DemographicData.objects.filter(questionnaire=self.questionnaire).order_by('order') )
            for a in arguments:
                # for each arguments, see if it matches a demographic data we seek
                for datum in data:
                    # the following jerryrigging is so that the regex specified
                    # matches the argument given in its entirety
                    regex = re.compile( '(%s)$' % datum.regex.strip().lower() )
                    match = regex.match( a )
                    if match:
                        if datum.type == 'i': # integer
                            val = int(match.group(0))
                        elif datum.type == 'c': # character
                            val = match.group(0)[0]
                        else:
                            val = match.group(0)
                        # we're good. save it!
                        if hasattr(self.user, datum.name):
                            setattr( self.user, datum.name, val)
                        # after we match the first time, we don't need to match again
                        data.remove(datum)
                        # we're done with this datum
                        break
        self.user.save()
        
    def _next_question(self,question):
        if question == None:
            return "thanks"
        return question.text

    def _first_access(self):
        return self.question == None

    def _is_trigger(self, message):
        for questionnaire in Questionnaire.objects.all():
            if message.strip().lower().startswith(questionnaire.trigger.strip().lower()):
                # todo - ro: move this to 'first access' once i understand better the 
                # relationship between usersession and questionnaire
                self.questionnaire = questionnaire
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
    


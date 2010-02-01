#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from django.db import models
from register.models import *
from reporters.models import PersistantConnection, PersistantBackend
from internationalization.utils import is_english

GENDER = ( ('M', 'Male'), ('F', 'Female') )

class Question(models.Model):
    question = models.CharField(null=False, max_length=200)

    def __unicode__(self):
        return self.question

    def flatten(self):
        choices = self.choice_set.all()
        responses = []

        for choice in choices:
            responses += [str(choice) for response in choice.pollresponse_set.all()]

        return [self.question, map(str,choices), responses]

class Choice(models.Model):
    choice = models.CharField(null=False, max_length=100)
    short_code = models.CharField(null=False, max_length=2)
    question = models.ForeignKey('Question')

    def __unicode__(self):
        return self.choice

class PollResponse(models.Model):
    issue = models.ForeignKey('Choice')
    age = models.IntegerField()
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER)
    mobile_number = models.IntegerField()
    location = models.CharField(max_length = 10)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null = True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null = True)
    governorate = models.IntegerField(null = True)
    district = models.IntegerField(null = True)

    def generate_response(self, text):
        try :
            parts = text.split(" ")
            self.issue = Choice.objects.get(short_code=parts[0])
            self.age = parts[1]
            self.gender = parts[2]
            self.save()
        except :
            raise ValueError("Sorry, we did not understand your response. Please re-send as - issue age gender area")
        return "Thank you for voting. You selected %s." % (self.issue)

    def set_location(self, registration):
        self.governorate = registration.governorate
        self.district = registration.district

    def __unicode__(self):
        return str(self.issue)+" "+str(self.age)+" "+str(self.gender)

class Phone(PersistantConnection):
    """ A phone registered with this poll. 
    Multiple individuals can share a phone, which is why it doesn't make
    sense to use the reporter app (which is targetted at individuals with
    multiple phones). At the same time, most people sharing a phone will
    speak the same language, so we can optionally associate phone with locale.
    
    """
    language = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return unicode( super(PersistantConnection, self) )
    
    @classmethod
    def from_message(klass, msg):
        obj, created = klass.objects.get_or_create(
            backend  = PersistantBackend.from_message(msg),
            identity = msg.connection.identity)
        
        if created:
            obj.save()
        
        if is_english(msg.text):
            obj.language = 'en'
        else:
            obj.language = 'ar'
            #conn.language = 'ar'#settings.LANGUAGE_CODE

        # just return the object. it doesn't matter
        # if it was created or fetched. TODO: maybe
        # a parameter to return the tuple
        return obj

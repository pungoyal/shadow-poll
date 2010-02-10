#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from django.db import models
from register.models import *
from reporters.models import PersistantConnection, PersistantBackend

GENDER = ( ('M', 'Male'), ('F', 'Female') )

class Question(models.Model):
    question = models.CharField(null=False, max_length=200)

    def __unicode__(self):
        return self.question

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
    mobile_number = models.CharField(max_length=20)
    location = models.CharField(max_length = 10)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null = True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null = True)
    governorate = models.IntegerField(null = True)
    district = models.IntegerField(null = True)

    def generate_response(self, text):
        try :
            parts = text.split(" ")
            self.issue = Choice.objects.get(short_code=parts[0].upper())
        except :
            raise ValueError("Not a poll response")
        try :
            self.age = parts[1]
            self.gender = parts[2]
            self.save()
        except :
            return "Sorry, we did not understand your response. Please re-send as - answer age gender"
        return "Thank you for voting. You selected %s." % (self.issue)

    def set_location(self, registration):
        self.governorate = registration.governorate
        self.district = registration.district

    def __unicode__(self):
        return str(self.issue)+" "+str(self.age)+" "+str(self.gender)

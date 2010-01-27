# -*- coding: utf-8 -*-
from django.db import models

class Governorate(models.Model):
    name = models.CharField(max_length = 100)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null = True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null = True)

class District(models.Model):
    name = models.CharField(max_length = 100)
    governorate = models.ForeignKey('Governorate')

class Registration(models.Model):
    public_identifier = models.CharField(max_length=10)
    governorate = models.IntegerField()
    district = models.IntegerField()
    mobile_number = models.IntegerField()
    
    def parse(self, message):
        parts = message.split(' ')
        self.public_identifier = parts[1]
        self.governorate = parts[2]
        self.district = parts[3]
        self.save()

    def __unicode__(self):
        return "%s %s %s %s" % (self.mobile_number, self.public_identifier, self.governorate, self.district)

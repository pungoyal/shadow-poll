# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from apps.reporters.models import PersistantConnection
from rapidsms.webui import settings

class Registration(models.Model):
    public_identifier = models.CharField(max_length=10)
    governorate = models.CharField(max_length=16)
    district = models.CharField(max_length=16)
    phone = models.ForeignKey(PersistantConnection)
    date = models.DateTimeField(default=datetime.now)
    
    def parse(self, message):
        parts = message.text.split(' ')
        self.public_identifier = parts[1]
        self.governorate = parts[2]
        self.district = parts[3]
        self.phone = message.persistant_connection
        self.save()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "%s %s %s %s" % (self.phone.identity, self.public_identifier, self.governorate, self.district)

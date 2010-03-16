# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from apps.reporters.models import PersistantConnection
from rapidsms.webui import settings
from charts.models import Governorate, District

class Registration(models.Model):
    public_identifier = models.CharField(max_length=10)
    phone = models.ForeignKey(PersistantConnection)
    date = models.DateTimeField(default=datetime.now)

    def _parse(self, message):
        parts = message.text.split(' ')
        if len(parts) < 4:
            return False
        self.public_identifier = parts[1]
        self.phone = message.persistant_connection
        self.phone.governorate = parts[2]
        self.phone.district = parts[3]
        return self

    def _validate_geographic_code(self, governorate_code, district_code):
        try:
            governorate = Governorate.objects.get(code = governorate_code)
        except Exception, ex:
            return False
        try:
            district = governorate.district_set.get(code = district_code)
        except Exception, ex:
            return False
        
        return True

    def _persist_registration_info(self):
        self.phone.save()
        self.save()

    def respond(self, message):
        registration_info = self._parse(message)
        if not registration_info:
            return "incorrect_register_format_error"
        
        user_phone = registration_info.phone
        if not self._validate_geographic_code(user_phone.governorate, user_phone.district):
            return "location_does_not_exist"
        
        self._persist_registration_info()
        return "initiate_poll_message"

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "%s %s" % (self.phone.identity, self.public_identifier)

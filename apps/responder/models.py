#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.db import models


class Responder(models.Model):
    trigger = models.CharField(max_length=30, help_text="The incoming message which triggers this responder")
    response = models.TextField()
    
    def __unicode__(self):
        return self.trigger

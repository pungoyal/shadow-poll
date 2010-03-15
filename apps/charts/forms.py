#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.forms import ModelForm
from apps.charts.models import VoiceMessage

class VoiceMessageForm(ModelForm):
    class Meta:
        model = VoiceMessage
        fields = ('english_text', 'arabic_text')

    def save(self, force_insert=False, force_update=False, commit=True):
        message = super(VoiceMessageForm, self).save(commit=False)
        message.translated = True
        message.save()
        return message

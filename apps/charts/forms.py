#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.forms import ModelForm, ValidationError
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

    def clean(self):
         cleaned_data = self.cleaned_data
         if 'english_text' not in cleaned_data or len(cleaned_data['english_text']) == 0 or \
             'arabic_text' not in cleaned_data or len(cleaned_data['arabic_text']) == 0: \
                raise ValidationError("Please provide both an English and an Arabic translation.")
         return cleaned_data;


#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from models import *
from reporters.models import Location, Reporter
from django.contrib.auth.models import User

class IaviReporterForm(forms.Form):

    participant_id = forms.CharField(min_length=3, max_length=3, required=True)
    location = forms.ModelChoiceField(Location.objects.all(), required=True)
    phone = forms.CharField(max_length=15, required=True)
    pin = forms.CharField(min_length=4, max_length=4, required=True)
    end_date = forms.DateField()
    
    def clean_pin(self):
        if not self.cleaned_data["pin"].isdigit():
            raise forms.ValidationError("PIN number must be 4 numeric digits.")
        return self.cleaned_data["pin"]

    def clean_participant_id(self):
        if not self.cleaned_data["participant_id"].isdigit():
            raise forms.ValidationError("Participant ID must be 3 numeric digits.")
        return self.cleaned_data["participant_id"]
    
    def clean_end_date(self):
        return self.cleaned_data["end_date"]
        

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        exclude = [ "email", "last_login", "date_joined", "is_staff", "is_active", "password", "user_permissions"]
    
class IaviProfileForm(forms.ModelForm):
    
    class Meta:
        model = IaviProfile
        exclude = [ "reporter" ]
    
    

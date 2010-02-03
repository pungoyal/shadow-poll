#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from models import *

class TreeForm(forms.ModelForms):
	class Meta:
		model = Tree

	def clean_alias(self):
		data = self.cleaned_data["trigger"]
		return data.lower()

class AnswerForm(forms.ModelForms):
	class Meta:
		model = Answer 

	def clean_alias(self):
		data = self.cleaned_data["trigger"]
		return data.lower()

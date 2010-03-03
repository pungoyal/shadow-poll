#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.contrib import admin
from apps.charts.models import Governorate, District, VoiceMessage

admin.site.register(Governorate)
admin.site.register(District)
admin.site.register(VoiceMessage)

#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.contrib import admin
from iavi.models import *

admin.site.register(IaviReporter)
admin.site.register(StudyParticipant)
admin.site.register(TestSession)
admin.site.register(KenyaReport)
admin.site.register(UgandaReport)
admin.site.register(Report)
admin.site.register(IaviProfile)

#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.contrib import admin
from questions.models import *

admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Option)
admin.site.register(Answer)

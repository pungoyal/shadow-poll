#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.contrib import admin
from tree.models import *

admin.site.register(Tree)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TreeState)
admin.site.register(Transition)
admin.site.register(Entry)
admin.site.register(Session)


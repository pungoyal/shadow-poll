#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.contrib import admin
from models import *

admin.site.register(Governorate)
admin.site.register(District)
admin.site.register(Registration)

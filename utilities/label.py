#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import datetime
#import settings 
#from django.core.management import setup_environ
#import os
# simple json is a python 2.5 library you need to install
# json comes bundled with python 2.6.  use one or the other
#import json

#setup_environ(settings)
from charts.models import Governorate, District

govs = Governorate.objects.all()
for gov in govs:
    gov.code = gov.id
    gov.save()
    districts = gov.district_set.all().order_by('name')
    i = 1
    for dis in districts:
         dis.code = i
         dis.save()
         i = i + 1


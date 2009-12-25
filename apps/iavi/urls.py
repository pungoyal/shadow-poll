#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import os
from django.conf.urls.defaults import *
import iavi.views as views

urlpatterns = patterns('',
    url(r'^iavi/?$', views.index),
    url(r'^iavi/compliance/?$', views.compliance),
    url(r'^iavi/data/?$', views.data),
    url(r'^iavi/users/?$', views.users),
    url(r'^iavi/users/(?P<id>\d*)/edit/?$', views.user_edit),
    url(r'^iavi/users/(?P<id>\d*)/change_password/?$', views.password_change),
    url(r'^iavi/users/new/?$', views.new_user),
    url(r'^iavi/participants/?$', views.participants),
    url(r'^iavi/participants/(?P<id>\d*)/?$', views.participant_summary),
    url(r'^iavi/participants/(?P<id>\d*)/edit/?$', views.participant_edit),
    
)

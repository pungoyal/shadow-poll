#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
import webapp.views as views

urlpatterns = patterns('',
    url(r'^ping$', views.check_availability),
    #override these login/logout pages with the ones in iraq app
    #(r'^accounts/login/$', "webapp.views.login"),
    #(r'^accounts/logout/$', "webapp.views.logout"),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)


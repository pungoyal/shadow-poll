#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import os
from django.conf.urls.defaults import *
import bednets.views as views

urlpatterns = patterns('',
    url(r'^locgen/?$', views.generate),
    url(r'^bednets/?$', views.index),
    url(r'^bednets/summary/(?P<locid>\d*)/?$', views.index),
    url(r'^bednets/json/?$', views.location_tree),
    url(r'^bednets/logistics/summary/(?P<locid>\d*)/?$', views.logistics_summary),
    url(r'^bednets/coupons/summary/(?P<locid>\d*)/?$', views.coupons_summary),
    url(r'^bednets/bednets/summary/(?P<locid>\d*)/?$', views.bednets_summary),
    url(r'^bednets/supply/summary/(?P<range>.*)/?(?P<from>.*)/?(?P<to>.*)/?$', views.supply_summary),
    url(r'^bednets/bednets/daily/(?P<locid>\d*)/?$', views.bednets_daily),
    url(r'^bednets/bednets/weekly/(?P<locid>\d*)/?$', views.bednets_weekly),
    url(r'^bednets/bednet/monthly/(?P<locid>\d*)/?$', views.bednets_monthly),
    url(r'^bednets/coupons/daily/(?P<locid>\d*)/?$', views.coupons_daily),
    url(r'^bednets/coupons/weekly/(?P<locid>\d*)/?$', views.coupons_weekly),
    url(r'^bednets/coupons/monthly/(?P<locid>\d*)/?$', views.coupons_monthly),
    url(r'^bednets/supply/daily/(?P<locid>\d*)/?$', views.supply_daily),
    url(r'^bednets/supply/weekly/(?P<locid>\d*)/?$', views.supply_weekly),
    url(r'^bednets/supply/monthly/(?P<locid>\d*)/?$', views.supply_monthly),
    url(r'^bednets/test/?$', views.index)
)

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import charts.views as chart_views

urlpatterns = patterns('',
                       url(r'^$',               chart_views.home_page),
                       url(r'^about/$',         direct_to_template, {'template':'about_poll.html'}),
                       url(r'^about/unicef$',   direct_to_template, {'template':'about_unicef.html'}),
                       url(r'^accounts/login/$', "webapp.views.login", {"template_name":"login.html"}),
                       url(r'^accounts/logout/$', "webapp.views.logout", {"template_name":"loggedout.html"}),
                       )

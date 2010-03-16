from django.conf.urls.defaults import *
import charts.views as views

urlpatterns = patterns('',
                       url(r'^$',     views.home_page),
                       )

from django.conf.urls.defaults import *
import charts.views as chart_views
import iraq.views as views

urlpatterns = patterns('',
                       url(r'^$',           chart_views.home_page),
                       url(r'^about/$',     views.about)
                       )

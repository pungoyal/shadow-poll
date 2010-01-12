from django.conf.urls.defaults import *
import charts.views as views

urlpatterns = patterns('',
    (r'^charts/$', views.currentStatus),
)

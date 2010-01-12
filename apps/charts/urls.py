from django.conf.urls.defaults import *
import charts.views as views

urlpatterns = patterns('charts',
                       (r'^/$', 'views.currentStatus'),
                       (r'^map/$', 'views.show_stats_on_map'),
                       )




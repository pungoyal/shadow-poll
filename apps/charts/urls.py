from django.conf.urls.defaults import *

urlpatterns = patterns('charts',
                       (r'^map/$', 'views.show_stats_on_map'),
                       ) 
from django.conf.urls.defaults import *
import charts.views as views

urlpatterns = patterns('charts',
                       (r'^charts/$', 'views.current_status'),
                       (r'^map/$', 'views.show_stats_on_map'),
                       )

urlpatterns += patterns('',
                        (r'^static/(?P<path>.*)$', 
                         'django.views.static.serve',
                         {'document_root': 'static'})
                         )
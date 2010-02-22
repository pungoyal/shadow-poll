from django.conf.urls.defaults import *
import charts.views as views

urlpatterns = patterns('charts',
                       (r'^charts/$', 'views.show_results'),
                       (r'^charts$', 'views.show_results'),
                       (r'^get_kml/$', 'views.get_governorates'),
                       (r'^charts/[qQ]uestion(\d{1,2})$', 'views.graphs'),
                       (r'^charts/(\d{1,2})$', 'views.show_governorate'),
                       (r'^charts/(\d{1,2})/(\d{1,2})$', 'views.show_district'),
                       (r'^graphs', 'views.show_graphs'),
                       )

handler404 = 'charts.views.view_404'
handler500 = 'charts.views.view_500'

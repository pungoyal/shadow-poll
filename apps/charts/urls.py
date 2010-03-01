from django.conf.urls.defaults import *
import charts.views as views

urlpatterns = patterns('charts',
                       (r'^charts/$', 'views.home_page'),
                       (r'^get_kml/(\d{1,2})$', 'views.get_kml_by_governorate'),
                       (r'^charts/[qQ]uestion?(\d{1,2})$', 'views.show_iraq_by_question'),
                       (r'^charts/(\d{1,2})/[qQ]uestion?(\d{1,2})$', 'views.show_governorate_by_question')
                       )

handler404 = 'charts.views.view_404'
handler500 = 'charts.views.view_500'

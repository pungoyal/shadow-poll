from django.conf.urls.defaults import *
import charts.views as views

urlpatterns = patterns('charts',
                       (r'^messages/audio/(.*)$', 'views.play_audio'),
                       url(r'^messages/translate/$', 'views.voice_admin_page', name="messages_admin"),
                       (r'^messages/$', 'views.voice_home_page'),
                       url(r'^message/translate/(\d+)$', 'views.voice_translate', name="translate_message"),
                       (r'^charts/[qQ]uestion?(\d+)/(\w+)/(\w+)/(\w+)/$', 'views.show_filtered_data_by_governorate_and_gender_and_age'),
                       (r'^charts/[qQ]uestion?(\d+)/(\w+)/(\w+)/$', 'views.show_filtered_data_by_governorate_and_gender'),
                       (r'^charts/[qQ]uestion?(\d+)/(\w+)/$', 'views.show_filtered_data_by_governorate'),
                       (r'^charts/[qQ]uestion?([\d+])/$', 'views.show_iraq_by_question'),
                       (r'^charts/$', 'views.home_page'),
                       (r'^get_kml/[qQ]uestion(\d+)/[gG]overnorate(\d{1,2})', 'views.kml_filtered_by_governorate'),
                       (r'^get_kml/[qQ]uestion(\d+)$', 'views.kml_filtered_by_country')
                       )

handler404 = 'charts.views.view_404'
handler500 = 'charts.views.view_500'

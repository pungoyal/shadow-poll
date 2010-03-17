from django.conf.urls.defaults import *
import charts.views as views

urlpatterns = patterns('charts',
                       (r'^messages/audio/(.*)$', 'views.play_audio'),
                       url(r'^messages/translate/$', 'views.voice_admin_page', name="messages_admin"),
                       (r'^messages/$', 'views.voice_home_page'),
                       url(r'^message/translate/(\d+)$', 'views.voice_translate', name="translate_message"),
                       (r'^charts/[qQ]uestion?(\d+)/[gG]overnorate(\d{1,2})', 'views.show_governorate_by_question'),
                       (r'^charts/[qQ]uestion?(\d+)$', 'views.show_iraq_by_question'),
                       (r'^charts/$', 'views.home_page'),
                       (r'^get_kml/[qQ]uestion(\d+)/[gG]overnorate(\d{1,2})', 'views.get_kml_for_governorate'),
                       (r'^get_kml/[qQ]uestion(\d+)$', 'views.get_kml_for_iraq')
                       )

handler404 = 'charts.views.view_404'
handler500 = 'charts.views.view_500'

from django.conf.urls.defaults import *
import charts.views as views

urlpatterns = patterns('charts',
                       (r'^messages/$', 'views.voice_home_page'),
                       url(r'^messages/translate/$', 'views.voice_admin_page', name="messages_admin"),
                       url(r'^message/translate/([0-9]+)$', 'views.voice_translate', name="translate_message"),
                       (r'^messages/audio/(.*)$', 'views.play_audio'),

                       (r'^charts/$', 'views.home_page'),

                       (r'^charts/[qQ]uestion?(\d{1,2})$', 'views.show_iraq_by_question'),
                       (r'^charts/[qQ]uestion?(\d{1,2})/[gG]overnorate(\d{1,2})', 'views.show_governorate_by_question'),
                       
                       (r'^charts/[qQ]uestion?(\d{1,2})/[mM]dg$', 'views.show_mdg'),

                       (r'^get_kml/[qQ]uestion(\d{1,2})$', 'views.get_kml_for_iraq'),
                       (r'^get_kml/[qQ]uestion(\d{1,2})/[gG]overnorate(\d{1,2})', 'views.get_kml_for_governorate')
                       )

handler404 = 'charts.views.view_404'
handler500 = 'charts.views.view_500'

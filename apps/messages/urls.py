from django.conf.urls.defaults import *
import messages.views as views

urlpatterns = patterns('messages',
                       (r'^messages/$', 'views.home_page')
                       )

handler404 = 'messages.views.view_404'
handler500 = 'messages.views.view_500'

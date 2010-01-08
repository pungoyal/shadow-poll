import views
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^iraq$', views.Dashboard),
)

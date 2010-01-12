from django.http import HttpRequest, HttpResponse
from django.template import loader, Context
from charts.models import Responses

import datetime

def show_stats_on_map(request):
    return HttpResponse("Hello World")

def current_status(self):
    now = datetime.datetime.now()
    template = loader.get_template('base.html')
    context = Context.({})
    html = "<html><body>Current time is %s.</body></html> " % now
    return HttpResponse(template.render(context))
    


from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from django.template import loader, Context
from charts.models import Responses

import datetime

def show_stats_on_map(request):
    return render_to_response('stats_map.html')

def current_status(self):
    now = datetime.datetime.now()
    template = loader.get_template('base.html')
    context = Context({
            'some_val':12,
            })
    html = "<html><body>Current time is %s.</body></html> " % now
    return HttpResponse(template.render(context))

from django.http import HttpRequest, HttpResponse
from charts.models import Responses
import datetime

def show_stats_on_map(request):
    return HttpResponse("Hello World")

def currentStatus(self):
    now = datetime.datetime.now()
    html = "<html><body>Current time is %s.</body></html> " % now
    return HttpResponse(html)
    


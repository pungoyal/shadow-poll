from django.http import HttpResponse
from charts.models import Responses
import datetime

def currentStatus(self):
    now = datetime.datetime.now()
    html = "<html><body>Current time is %s.</body></html> " % now
    return HttpResponse(html)
    
    

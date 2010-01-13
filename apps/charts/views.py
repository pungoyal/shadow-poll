from django.http import HttpRequest, HttpResponse, HttpResponseNotFound,\
    HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import loader, Context
from charts.chart_data import ChartData
from django.template.context import RequestContext

import datetime

def show_stats_on_map(request):
    return render_to_response('stats_map.html')

def current_status(self):
    now = datetime.datetime.now()
    return render_to_response('charts.html')

def data(self):
    return HttpResponse('junk')
    
def view_404(request):
    response = HttpResponseNotFound()
    response.write("The path is not found")
    return response

def view_500(request):
    response = HttpResponseServerError()
    response.write("Something went wrong")
    return response


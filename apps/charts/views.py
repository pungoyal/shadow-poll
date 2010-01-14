from django.http import HttpRequest, HttpResponse, HttpResponseNotFound,\
    HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import loader, Context
from charts.chart_data import ChartData
from django.template.context import RequestContext
from httplib import HTTPResponse
import urllib2

import datetime

def show_stats_on_map(request):
    return render_to_response('stats_map.html')

def get_stats(request):
    if request.method == 'GET':
        left = request.GET.get('left')
        bottom = request.GET.get('bottom')
        right = request.GET.get('right')
        top = request.GET.get('top')
        x = request.GET.get('x')
        y = request.GET.get('y')
        url = ("http://localhost/geoserver/wms/reflector?bbox=%s,%s,%s,%s&\
format=jpeg&info_format=text/plain&request=GetFeatureInfo&layers=GADM:IRQ_adm2&\
query_layers=GADM:IRQ_adm2&width=550&height=250&x=%s&y=%s" % (left, bottom, right, top, x, y))
        request = urllib2.urlopen(url)
        response_dict = request.read()
        print response_dict
        return HttpResponse("OK")
        

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


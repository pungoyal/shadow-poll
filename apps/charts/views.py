from math import sqrt

from charts.models import Governorates
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import loader

def get_governorates(request):
    reports = Governorates.objects.kml()
    scales = [sqrt(i * 0.1) for i in range(1, 200)]
    style = 'kml/population_points.kml'
    r = _render_to_kml('kml/placemarks.kml', {'places' : reports, 'scales' : scales, 'style' : style})
    r['Content-Disposition'] = 'attachment;filename=reports.kml'
    return r

def show_governorate(request, governorate_id):
    response = HttpResponse()
    g = Governorates.objects.filter(id=governorate_id).iterator().next()
    
    response.write(g)
    return response

def show_results(request):
    return render_to_response('map.html')

def view_404(request):
    response = HttpResponseNotFound()
    response.write("The path is not found")
    return response

def view_500(request):
    response = HttpResponseServerError()
    response.write("Something went wrong")
    return response

def _render_to_kml(*args, **kwargs):
    "Renders the response as KML (using the correct MIME type)."
    return HttpResponse(loader.render_to_string(*args, **kwargs), mimetype='application/vnd.google-earth.kml+xml')

def show_district(request, governorate_id, district_id):
    response = HttpResponse()
    response.write("Under Construction. Come back soon, please :)")
    return response

from math import sqrt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.template import loader
from rapidsms.webui.utils import render_to_response

from apps.charts.models import Governorates
from apps.tree.models import Question

def get_governorates(request):
    reports = Governorates.objects.kml()
    scales = [sqrt(i * 0.1) for i in range(1, 20)]
    style = 'kml/population_points.kml'
    r = _render_to_kml('kml/placemarks.kml', {'places' : reports, 'scales' : scales, 'style' : style})
    r['Content-Disposition'] = 'attachment;filename=reports.kml'
    return r

def graphs(request, question_number):
    question = Question.objects.get(id=question_number)
    response_break_up = question.response_break_up()
    
    return render_to_response(request, "results.html", {"break_up": response_break_up})

def show_governorate(request, governorate_id):
    try:
        governorate = Governorates.objects.get(id=governorate_id)
    except:
        return HttpResponseServerError("Sorry, governorate not found")

    return render_to_response(request, 'results.html', {"bbox": governorate.bounding_box})

def home_page(request):
    response = HttpResponse()
    response.write("<h1>Homepage coming soon. </h1>")
    response.write("Head to <a href='question1'>Question 1</a> page")
    return response

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

from math import sqrt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.template import loader
from rapidsms.webui.utils import render_to_response

from apps.charts.models import Governorate
from apps.poll.models import Question, Choice, Color

from django.utils.cache import patch_vary_headers
from django.utils import translation

def get_governorates(request, question_number):
    reports = Governorate.objects.kml()
    question = Question.objects.get(id=question_number)
    placemarks_info_list = []
    for governorates in reports:
        placemarks_info_list.append({'id': governorates.id, 'name': governorates.name, 'description': governorates.description, 'kml': governorates.kml, 'style': governorates.style(question)})
    colors = Color.objects.all()
    scales = [sqrt(i * 0.1) for i in range(1, 20)]
    style = 'kml/population_points.kml'
    r = _render_to_kml('kml/placemarks.kml', {'places' : placemarks_info_list, 'scales' : scales, 'style' : style, 'colors': colors})
    r['Content-Disposition'] = 'attachment;filename=reports.kml'
    return r

def graphs(request, question_number):
    question = Question.objects.get(id=question_number)
    choices = Choice.objects.filter(question=question)
    response_break_up = question.response_break_up()

    language = get_language_from_request(request)
    translation.activate(language)
    current_language = translation.get_language()
    
    return render_to_response(request, "results.html", {"chart_data": response_break_up, "national_data": response_break_up, "region": "Iraq", "top_response": "Security", "percentage": "64", "question": question, "choices": choices,"stylesheetlang": current_language})

def get_language_from_request(request):
    from rapidsms.webui import settings
    supported = dict(settings.LANGUAGES)
    if hasattr(request, 'session'):
        lang_code = request.session.get('django_language', None)
        if lang_code in supported and lang_code is not None:
            return lang_code
    return settings.LANGUAGE_CODE

def show_governorate(request, governorate_id):
    governorate = Governorate.objects.get(id=governorate_id)
    return render_to_response(request, 'results.html', {"bbox": governorate.bounding_box, "chart_data": []})

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

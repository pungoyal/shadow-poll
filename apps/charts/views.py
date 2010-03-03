from math import sqrt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import translation

from rapidsms.webui.utils import render_to_response

from apps.charts.models import Governorate, Audio
from apps.poll.models import Question, Choice, Color

def voice_home_page(request):
    audio_files = Audio.objects.all()
    return render_to_response(request, "messages.html", {"audio": audio_files})

def show_governorate(request, governorate_id):
    governorate = Governorate.objects.get(id=governorate_id)
    return render_to_response(request, 'results.html', {"bbox": governorate.bounding_box, "chart_data": []})

def home_page(request):
    response = HttpResponse()
    response.write("<h1>Homepage coming soon. </h1>")
    response.write("Head to <a href='question1'>Question 1</a> page")
    return response

def show_iraq_by_question(request, question_number, 
                          template='results.html', context={}):
    question = get_object_or_404(Question, pk=question_number)
    choices_of_question = Choice.objects.filter(question = question)
    categories = [choice.category for choice in choices_of_question]
    response_break_up = question.response_break_up()
    context.update(   {"chart_data": response_break_up, 
                       "national_data": response_break_up, 
                       "region": "Iraq", 
                       # TODO - fix
                       "top_response": "Security", 
                       "percentage": "64",
                       "question": question, 
                       "choices": Choice.objects.filter(question=question),
                       "categories": categories
                       })    
    return render_to_response(request, template, context)

def show_governorate_by_question(request, governorate_id, question_number, 
                                 template='results.html', context={}):
    question = get_object_or_404(Question, pk=question_number)
    response_break_up = question.response_break_up(governorate_id)
    governorate = get_object_or_404(Governorate, pk=governorate_id)
    context.update(   {"chart_data": response_break_up, 
                       "national_data": response_break_up, 
                       "region": governorate.name, 
                       # TODO - fix
                       "top_response": "Security", 
                       "percentage": "64", 
                       "bbox": governorate.bounding_box,
                       "question": question, 
                       "choices": Choice.objects.filter(question=question)
                       })
    return render_to_response(request, template, context)

def view_404(request):
    response = HttpResponseNotFound()
    response.write("The path is not found")
    return response

def view_500(request):
    response = HttpResponseServerError()
    response.write("Something went wrong")
    return response

def get_kml_by_governorate(request, question_number):
    reports = Governorate.objects.kml()
    question = Question.objects.get(id=question_number)
    placemarks_info_list = []
    style_dict_list = []
    for (counter, governorates) in enumerate(reports):
        style_dict = governorates.style(question)
        if style_dict:
            style_str = "s%s-%d" % (style_dict['color'].id, len(style_dict_list))
            placemarks_info_list.append({'id': governorates.id,
                                     'name': governorates.name, 
                                     'description': governorates.description, 
                                     'kml': governorates.kml, 
                                     'style': style_str})
            style_dict_list.append({'id': style_dict['color'].id, 'percentage': style_dict['percentage'], 'file_name': style_dict['color'].file_name})
    colors = Color.objects.all()
    style = 'kml/population_points.kml'
    r = _render_to_kml('kml/placemarks.kml', {'places' : placemarks_info_list, 
                                              'style_dict_list' : style_dict_list, 
                                              'style' : style})
    r['Content-Disposition'] = 'attachment;filename=reports.kml'
    return r

def _render_to_kml(*args, **kwargs):
    "Renders the response as KML (using the correct MIME type)."
    return HttpResponse(loader.render_to_string(*args, **kwargs), 
                        mimetype='application/vnd.google-earth.kml+xml')


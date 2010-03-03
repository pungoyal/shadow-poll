from math import sqrt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import translation

from rapidsms.webui.utils import render_to_response

from apps.charts.models import Governorate, District, Audio
from apps.poll.models import Question, Choice, Color

def voice_home_page(request):
    audio_files = Audio.objects.all()
    return render_to_response(request, "messages.html", {"audio": audio_files})

def show_governorate(request, governorate_id, template='results.html'):
    governorate = Governorate.objects.get(id=governorate_id)
    return render_to_response(request, template, 
                              {"bbox": governorate.bounding_box, 
                               "governorate": governorate,
                                "chart_data": []
                               })

def show_iraq_by_question(request, question_id, 
                          template='results.html', context={}):
    context.update(   {"region": "Iraq", 
                       # TODO - fix
                       "top_response": "Security", 
                       "percentage": "64",
                       })    
    return show_by_question(request, question_id, template, context)

def show_governorate_by_question(request, governorate_id, question_id, 
                                 template='results.html', context={}):
    governorate = get_object_or_404(Governorate, pk=governorate_id)
    question = get_object_or_404(Question, pk=question_id)
    response_break_up = question.response_break_up(governorate_id)
    context.update(   {"region": governorate.name, 
                       "chart_data": response_break_up, 
                       # TODO - fix
                       "top_response": "Security", 
                       "percentage": "64", 
                       "governorate": governorate,
                       "bbox": governorate.bounding_box,
                       })
    return show_by_question(request, question_id, template, context)

def show_by_question(request, question_id, template, context={}):
    question = get_object_or_404(Question, pk=question_id)
    national_response_break_up = question.response_break_up()
    choices_of_question = Choice.objects.filter(question = question)
    categories = [choice.category for choice in choices_of_question]
    context.update( {"categories": categories,
                    "question": question, 
                    "national_data": national_response_break_up, 
                    "choices": Choice.objects.filter(question=question)
                    })
    if 'chart_data' not in context:
        # if chart_data not set, default to national view
        context.update( {"chart_data": national_response_break_up}) 
    return render_to_response(request, template, context)

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

def get_kml_for_governorate(request, governorate_id, question_id):
    gov = Governorate.objects.get(pk=governorate_id)
    district_kml = District.objects.filter(governorate=gov).kml()
    return get_kml(request, question_id, district_kml)

def get_kml_for_iraq(request, question_id):
    governorate_kml = Governorate.objects.kml()
    return get_kml(request, question_id, governorate_kml)

def get_kml(request, question_id, kml):
    """ the kml tells us where to center our bubbles on the map """
    question = Question.objects.get(id=question_id)
    placemarks_info_list = []
    style_dict_list = []
    for (counter, governorates) in enumerate(kml):
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
    r['Content-Disposition'] = 'attachment;filename=boundaries.kml'
    return r

def _render_to_kml(*args, **kwargs):
    "Renders the response as KML (using the correct MIME type)."
    return HttpResponse(loader.render_to_string(*args, **kwargs), 
                        mimetype='application/vnd.google-earth.kml+xml')

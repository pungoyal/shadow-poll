import os, mimetypes, operator

from math import sqrt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError,Http404,\
    HttpRequest
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import translation, simplejson

from rapidsms.webui import settings
from rapidsms.webui.utils import render_to_response

from apps.charts.models import Governorate, District, VoiceMessage
from apps.poll.models import Question, Choice, Color

def voice_home_page(request):
    messages = VoiceMessage.objects.all()
    return render_to_response(request, "messages.html", {"messages": messages})

def play_audio(request, file_name):
    media_dir = settings.RAPIDSMS_APPS["charts"]["media_dir"]
    abspath = os.path.join(media_dir, file_name)

    if not os.path.exists(abspath):
        raise Http404("Could not find media '%s' at location '%s'" % (file_name, media_dir))

    mimetype = mimetypes.guess_type(abspath)[0] or 'application/octet-stream'
    contents = open(abspath, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Content-Length"] = len(contents)
    return response

def show_governorate(request, governorate_id, template='results.html'):
    governorate = Governorate.objects.get(id=governorate_id)
    return render_to_response(request, template,
                              {"bbox": governorate.bounding_box,
                               "governorate": governorate,
                               "chart_data": []
                              })

def show_iraq_by_question(request, question_id,
                          template='results.html'):
    context = {}
    context.update({"region": "Iraq"})
    return show_by_question(request, question_id, None, template, context)

def show_governorate_by_question(request, governorate_id, question_id,
                                 template='results.html'):
    context = {}
    governorate = get_object_or_404(Governorate, pk=governorate_id)
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question)
    for choice in choices:
        choice.num_votes = choice.num_votes(governorate)
    context.update(   {"region": governorate.name,
                       "governorate": governorate,
                       "bbox": governorate.bounding_box,
                       "choices": choices})
    return show_by_question(request, question_id, governorate_id, template, context)

def show_by_question(request, question_id, governorate_id, template, context={}):
    question = get_object_or_404(Question, pk=question_id)
    national_response_break_up = question.response_break_up()
    response_break_up = question.response_break_up(governorate_id)

    if len(response_break_up) == 0:
        response_break_up.append("No reponses yet")
        response_break_up.append(0)

    choices_of_question = Choice.objects.filter(question = question)
    categories = question.get_categories()

    character_english =  ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                          'h', 'i', 'j', 'k', 'l', 'm', 'n']

    #finding the highest voted response
    top_response = response_break_up[0]
    for break_up in response_break_up:
        if(break_up.percentage > top_response.percentage):
            top_response = break_up

    context.update( {"categories": categories,
                     "question": question,
                     "top_response": top_response,
                     "chart_data": simplejson.dumps([r.__dict__ for r in response_break_up]),
                     "national_data": simplejson.dumps([r.__dict__ for r in national_response_break_up]),
                     "character_english": character_english,
                     "questions" : Question.objects.all()
    }) 
    if 'chart_data' not in context:
    # if chart_data not set, default to national view
        context.update( {"chart_data": national_response_break_up})
    if 'choices' not in context:
        context.update( {"choices": choices_of_question} )
    return render_to_response(request, template, context)

def home_page(request):
    response = HttpResponse()
    response.write("<h1>Homepage coming soon. </h1>")
    response.write("Head to <a href='question1?gender=m,f&age=a1,a2,a3'>Question 1</a> page")
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
    #betnada in arabic
    governorate_kml = Governorate.objects.kml()
    return get_kml(request, question_id, governorate_kml)

def get_kml(request, question_id, kml):
    """ the kml tells us where to center our bubbles on the map """
    question = Question.objects.get(id=question_id)
    placemarks_info_list = []
    style_dict_list = []
    gender = request.GET.get('gender')
    age = request.GET.get('age')
    print gender 
    selected_options={}
    
    if gender <>"" :
        selected_options["gender"] = gender
    if gender =="":
        selected_options["gender"] = ""
    
    if age <> "" :
        selected_options["age"] = age
    if age == "" :
        selected_options["age"] = ""

    for (counter, geography) in enumerate(kml):
        style_dict = geography.style(question,selected_options)
        if style_dict:
            style_str = "s%s-%d" % (style_dict['color'].id, len(style_dict_list))
            placemarks_info_list.append({'id': geography.id,
                                         'name': geography.name,
                                         'description': geography.description,
                                         'kml': geography.kml,
                                         'style': style_str})
            style_dict_list.append({'id': style_dict['color'].id, 'percentage': style_dict['percentage'],
                                    'file_name': style_dict['color'].file_name})
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

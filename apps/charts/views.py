import os, mimetypes, operator

from math import sqrt
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError,Http404,\
    HttpRequest
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import translation, simplejson
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from rapidsms.webui import settings
from rapidsms.webui.utils import render_to_response

from apps.charts.models import Governorate, District, VoiceMessage
from apps.charts.forms import VoiceMessageForm
from apps.poll.models import Question, Choice, Color, UserResponse
from apps.charts.breakups import ResponseBreakUp, ChoiceBreakUp

character_english =  ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                          'h', 'i', 'j', 'k', 'l', 'm', 'n']


def home_page(request, template = "home_page.html"):
    questions = Question.objects.all()
    return render_to_response(request, template, {'questions' : questions})

def voice_home_page(request):
    messages = VoiceMessage.objects.filter(translated=True).order_by('-date_recorded')
    return render_to_response(request, "messages.html", 
                              {"messages": messages, 
                               "questions": Question.objects.all().order_by('pk')})

@login_required
def voice_admin_page(request):
    context = {}
    messages = VoiceMessage.objects.filter(translated=False)
    context['num_translated_messages'] = messages.count()
    context["messages"] = messages.order_by('-date_recorded')[:5]
    return render_to_response(request, "translate_messages.html", context)

@login_required
def voice_translate(request, message_id, template = "translate_message.html"):
    context = {}
    message = get_object_or_404(VoiceMessage, pk=message_id)
    if request.method == "POST":
        form = VoiceMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            context['status'] = _("Translation saved.")
    else:
        form = VoiceMessageForm(instance=message)
    context['form'] = form
    context['message'] = message
    return render_to_response(request, template, context)

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


def show_iraq_by_question(request, question_id,
                          template='results.html'):
    context = {}
    context.update({"region": "Iraq"})
    return _update_context_with_data(request, question_id, None, template, context)
    
def show_filtered_data_by_governorate(request, question_id, governorate_id,
                                      template='results.html'):
    
    context = {}
    governorate_id = _sanitize_governorate_id(governorate_id)
    _update_context_for_governorate(context, governorate_id)
    return _update_data_with_filters_applied(request, question_id, governorate_id, template, context)

def _update_data_with_filters_applied(request, question_id, governorate_id, template, context):
    filter_dict = {'gender': None, 'age': None}
    for key in request.GET:
        filter_dict[key] = request.GET[key]
    context.update({
            "gender_filter": filter_dict['gender'],
            "age": filter_dict['age']
            })
    gender = _sanitize_gender_identifier(filter_dict['gender'])
    agegroup = []
    if filter_dict['age'] is not None:
        ranges = filter_dict['age'].split(',')
        for age_ranges in ranges:
            agegroup.append(age_ranges)

    age_group_list = _sanitize_age_group(agegroup)
    return _update_context_with_data(request, question_id, governorate_id, template, context, gender, age_group_list)

def _sanitize_governorate_id(governorate_id):
    if governorate_id == "all" : 
        return None
    else:
        return governorate_id.replace("governorate","")

def _sanitize_gender_identifier(gender):
    if gender == "boys":
        return "m"
    if gender == "girls":
        return "f"
    return None

def _sanitize_age_group(age_group):
    ages = []
    for age in age_group:
        ages.append(age.split("to"))
    return ages

def _update_context_for_governorate(context,governorate_id):
    if(governorate_id != None):
        governorate_id = governorate_id.replace("governorate","")
        governorate = get_object_or_404(Governorate, pk=governorate_id)
        context.update(   {"region": governorate.name,
                           "governorate": governorate,
                           "bbox": governorate.bounding_box,
                           })
    else:
        context.update({"region": "iraq"})

def _update_context_with_data(request, question_id, governorate_id,template, context={}, gender=None, age_group_list=None):
    question = get_object_or_404(Question, pk=question_id)
    national_response_break_up = question.response_break_up()
    response_break_up = question.response_break_up(governorate_code = governorate_id, gender = gender, age_group_list = age_group_list)

    choices_of_question = Choice.objects.filter(question = question)
    categories = question.get_categories()

    total_responses = sum([response_for_category["votes"] for response_for_category in response_break_up["by_category"]])

    response_by_category = ResponseBreakUp.create_from(response_break_up["by_category"], categories)

    national_response_by_category = ResponseBreakUp.create_from(national_response_break_up["by_category"], categories)

    response_by_choice = ChoiceBreakUp.create_from(response_break_up["by_choice"], choices_of_question)

    top_response = response_by_category[0]

    context.update( {"categories": categories,
                     "choices" : response_by_choice,
                     "question": question,
                     "top_response": top_response,
                     "total_responses" : total_responses,
                     "chart_data": simplejson.dumps([r.__dict__ for r in response_by_category]),
                     "national_data": simplejson.dumps([r.__dict__ for r in national_response_by_category]),
                     "character_english": character_english,
                     "questions" : Question.objects.all()
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

def kml_filtered_by_governorate(request, question_id, governorate_id):
    gov = Governorate.objects.get(pk=governorate_id)
    district_kml = District.objects.filter(governorate=gov).kml()
    return get_kml(request, question_id, district_kml, gov)

def kml_filtered_by_country(request, question_id):
    filter_dict = {'gender': None, 'age': None}
    for key in request.GET:
        filter_dict[key] = request.GET[key]
    gender = _sanitize_gender_identifier(filter_dict['gender'])
    agegroup = []
    if filter_dict['age'] is not None:
        ranges = filter_dict['age'].split(',')
        for age_ranges in ranges:
            agegroup.append(age_ranges)
    age_group_list = _sanitize_age_group(agegroup)
    governorate_kml = Governorate.objects.kml()
    return get_kml(request, question_id, governorate_kml, governorate = None, gender = gender, age_group_list = age_group_list)

def get_kml(request, question_id, kml, governorate, gender=None, age_group_list = None):
    """ the kml tells us where to center our bubbles on the map """
    question = Question.objects.get(id=question_id)
    placemarks_info_list = []
    style_dict_list = []
    for (counter, geography) in enumerate(kml):
        if governorate is not None:
            response_break_up = question.response_break_up(governorate_code = governorate.code, district_code = geography.code, gender = gender, age_group_list = age_group_list)
        else:
            response_break_up = question.response_break_up(governorate_code = geography.code, gender = gender, age_group_list = age_group_list)
        categories = question.get_categories()
        total_responses = sum([response_for_category["votes"] for response_for_category in response_break_up["by_category"]])
        if total_responses > 0:
            response_by_category = ResponseBreakUp.create_from(response_break_up["by_category"], categories)
            top_response = response_by_category[0]
            color = Color.objects.get(code = top_response.color)
            style_str = "s%s-%d" % (top_response.color, len(placemarks_info_list))
            placemarks_info_list.append({'id': geography.id,
                                         'name': geography.name,
                                         'description': geography.description,
                                         'kml': geography.kml,
                                         'style': style_str})
            style_dict_list.append({'id': top_response.color, 'percentage': top_response.percentage/100,
                                    'file_name': color.file_name})
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

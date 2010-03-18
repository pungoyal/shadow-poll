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

character_english =  ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                          'h', 'i', 'j', 'k', 'l', 'm', 'n']


def home_page(request, template = "home_page.html"):
    questions = Question.objects.all()
    return render_to_response(request, template, {'questions' : questions})

def voice_home_page(request):
    messages = VoiceMessage.objects.all()
    return render_to_response(request, "messages.html", 
                              {"messages": messages, 
                               "questions": Question.objects.all().order_by('pk')})

@login_required
def voice_admin_page(request):
    messages = VoiceMessage.objects.filter(translated = False).order_by('-date_recorded')[:5]
    context = {}
    context['num_translated_messages'] = VoiceMessage.objects.filter(translated=True).count()
    context["messages"] = messages
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
            context['status'] = _(form.errors)
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
    return show_by_question(request, question_id, None, template, context)
    
def show_filtered_data_by_governorate(request, question_id, governorate_id,
                                      template='results.html'):

    context = {}
    if(governorate_id != "all"):
        governorate_id = governorate_id.replace("governorate","")
        _update_context_for_governorate(context, governorate_id)

    return show_by_question(request, question_id, governorate_id, template, context)

def _update_context_for_governorate(context,governorate_id):
    governorate = get_object_or_404(Governorate, pk=governorate_id)

    context.update(   {"region": governorate.name,
                       "governorate": governorate,
                       "bbox": governorate.bounding_box,
                       })

class ResponseBreakUp():
    #FAAFBE is the default color that shows up when there are no responses for a level
    def __init__(self, text=_("No responses yet"), percentage=0, color="#FAAFBE"):
        self.percentage = percentage
        self.color = color
        self.text = text

    @classmethod
    def create_from(klass, responses, categories):
        breakups = []
        total_responses = sum([response_for_category["votes"] for response_for_category in responses])

        if len(responses) == 0:
            return [ResponseBreakUp(text = "No responses yet")]


        for response in responses:
            category = filter(lambda cat: cat.id == response["choice__category"], categories)[0]
            breakup  = ResponseBreakUp(percentage = round(response["votes"]*100/total_responses,1), color = category.color.code, text = category.name )
            breakups.append(breakup)
        return breakups


class ChoiceBreakUp():
    #FAAFBE is the default color that shows up when there are no responses for a level
    def __init__(self, text=_("No responses yet"), votes=0, color="#FAAFBE"):
        self.votes = votes
        self.color = color
        self.text = text

    @classmethod
    def create_from(klass, responses, choices):
        breakups = []
        for choice in choices :
            response = filter(lambda r : r["choice"] == choice.id, responses)
            breakup = ChoiceBreakUp(votes = response[0]["votes"] if len(response) > 0 else 0, color = choice.category.color, text = choice.text )
            breakups.append(breakup)
        return breakups


def show_by_question(request, question_id, governorate_id, template, context={}):
    question = get_object_or_404(Question, pk=question_id)
    national_response_break_up = question.response_break_up()
    response_break_up = question.response_break_up(governorate_id)
    choices_of_question = Choice.objects.filter(question = question)
    categories = question.get_categories()


    total_responses = sum([response_for_category["votes"] for response_for_category in response_break_up["by_category"]])


    response_by_category = ResponseBreakUp.create_from(response_break_up["by_category"], categories)

    response_by_choice = ChoiceBreakUp.create_from(response_break_up["by_choice"], choices_of_question)

    top_response = response_by_category[0]

    context.update( {"categories": categories,
                     "choices" : response_by_choice,
                     "question": question,
                     "top_response": top_response,
                     "total_responses" : total_responses,
                     "chart_data": simplejson.dumps([r.__dict__ for r in response_by_category]),
                     "national_data": simplejson.dumps([r.__dict__ for r in response_by_category]),
                     "character_english": character_english,
                     "questions" : Question.objects.all()
    }) 

    return render_to_response(request, template, context)



def show_filtered_data_by_governorate_and_gender(request, question_id, governorate_id, gender,template='results.html'):
    context = {}
    total_responses = len(UserResponse.objects.all())
    question = get_object_or_404(Question, pk=question_id)
    context.update({"region": "Iraq", 
                    'total_responses': total_responses})
    return show_by_question(request, question_id, None, template, context)

def show_filtered_data_by_governorate_and_gender_and_age(request, question_id, governorate_id,gender,age_group,template='results.html'):
    context = {}
    total_responses = len(UserResponse.objects.all())
    question = get_object_or_404(Question, pk=question_id)
    context.update({"region": "Iraq", 
                    'total_responses': total_responses})
    return show_by_question(request, question_id, None, template, context)



def view_404(request):
    response = HttpResponseNotFound()
    response.write("The path is not found")
    return response

def view_500(request):
    response = HttpResponseServerError()
    response.write("Something went wrong")
    return response

def get_kml_for_governorate(request, question_id, governorate_id):
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
    for (counter, geography) in enumerate(kml):
        style_dict = geography.style(question)
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

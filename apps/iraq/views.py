from apps.poll.models import Question
from rapidsms.webui.utils import render_to_response

def about(request, template = "about.html"):
    questions = Question.objects.all()
    return render_to_response(request, template, {'questions' : questions})

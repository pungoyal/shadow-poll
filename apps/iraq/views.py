from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from iraq.models import *


def Dashboard(request):
    return HttpResponse("hello")


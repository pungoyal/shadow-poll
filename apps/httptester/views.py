# vim: ai ts=4 sts=4 et sw=4

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from rapidsms.webui.utils import render_to_response
from django.core.urlresolvers import reverse
from rapidsms.webui import settings
import datetime
import urllib
import urllib2
import random

def index(req):
    template_name="http/ajaxified.html"
    return render_to_response(req, template_name, {
    })

def proxy(req):
    # build the url to the http server running
    # in ajax.app.App via conf hackery
    conf = settings.RAPIDSMS_APPS["httptester"]
    url = "http://%s:%s/" % (
        conf["host"], 
        conf["port"]
    )
    data = _dict_to_string(req.POST)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return HttpResponse(response.read())

def _dict_to_string(dict_):
    """ Convert dictionary structure to key-value pair string 
    e.g. {'a':'b', 'c':'d'} -> a=b&c=d
    """
    return "&".join(['%s=%s' % (key, dict_[key]) for key in dict_])
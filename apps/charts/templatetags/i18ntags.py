from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_languages():
    html = ""
    for key,value in settings.LANGUAGES:
        lang_html= "<option value=\""
        lang_html += key
        lang_html +="\">"
        lang_html += value
        lang_html += "</option>"
        html += lang_html
    return html
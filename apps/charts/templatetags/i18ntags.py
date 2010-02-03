from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_languages():
    html = ""
    print settings.LANGUAGE_CODE
    for key,value in settings.LANGUAGES:
        lang_html= "<a href=\"javascript:test('"
        lang_html += key
        lang_html +="')\">"
        lang_html += value
        lang_html += "</a>"
        lang_html += " | "
        html += lang_html
    return html[:-2]
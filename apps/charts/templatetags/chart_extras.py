from django import template

register = template.Library()

@register.filter
def dict_lookup(dict, key):
    return dict.get(key)

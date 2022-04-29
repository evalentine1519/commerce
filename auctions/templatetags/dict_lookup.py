from django.template.defaultfilters import register
from django import template

register = template.Library()

@register.filter(name='dict_lookup')
def dict_lookup(d, k):
    return d.get(k)
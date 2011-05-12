from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr)

@register.filter
def rmnone(str):
    return str or ''

@register.filter
def rmnonenum(num):
    return num or 0

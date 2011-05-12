from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr)

@register.filter
def rmnone(str):
    return str or ''

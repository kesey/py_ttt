from django import template

register = template.Library()

@register.filter
def value_from_key(dictionnary:dict, key):
    return dictionnary[key]

@register.filter
def addf(value, arg):
    return float(value) + float(arg)
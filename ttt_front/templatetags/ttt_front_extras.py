from django import template

register = template.Library()

@register.filter
def value_from_key(dictionnary:dict, key):
    return dictionnary[key]
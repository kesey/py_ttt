from django import template

register = template.Library()

@register.filter
def startswith(text:str, starts:str):
    return text.startswith(starts)
    
@register.filter
def truncstart(text:str, num:int):
    return text[num:]

@register.filter
def zero_display(value):
    return value if value else 0.00
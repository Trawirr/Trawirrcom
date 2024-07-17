from django import template

register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter(name='card_url')
def card_url(card_name):
    return f"{card_name}-home"
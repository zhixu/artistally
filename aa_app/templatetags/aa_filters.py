from django import template

register = template.Library()

@register.filter
def for_convention(stuff, con):
    return stuff.filter(convention = con)

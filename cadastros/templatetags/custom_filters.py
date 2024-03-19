from django import template

register = template.Library()

@register.filter
def get_item(obj, key):
    if hasattr(obj, key):
        return getattr(obj, key)
    else:
        return ''

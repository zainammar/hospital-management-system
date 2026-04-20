from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value, arg):
    """
    Usage: {{ value|replace:"old,new" }}
    """
    if len(arg.split(',')) != 2:
        return value
    old, new = arg.split(',')
    return str(value).replace(old, new)
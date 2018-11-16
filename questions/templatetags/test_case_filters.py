from django import template

register = template.Library()

@register.filter
def comma2newline(datetime):
    datetime = str(datetime)
    datetime.replace(",", "\n")
    return datetime
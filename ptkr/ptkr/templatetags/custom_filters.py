from django import template

register = template.Library()

@register.filter
def percent(value):
    try:
        return f"{float(value) * 100:.2f}%"
    except (ValueError, TypeError):
        return ""

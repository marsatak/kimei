from django import template
import datetime

register = template.Library()


@register.filter(name='seconds_to_hm')
def seconds_to_hm(value):
    if value is None:
        return "00:00"  # ou une autre valeur par défaut que vous préférez
    try:
        total_seconds = int(value)
    except (ValueError, TypeError):
        return "00:00"  # ou retournez la valeur originale si vous préférez : `return value`
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

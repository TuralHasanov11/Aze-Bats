from django import template
from apps.home.models import StaticText

register = template.Library()

@register.simple_tag
def get_static_text(key, language='az') -> str:
    static_text = StaticText.entries.single(key, language)
    return static_text.content if static_text else '' 
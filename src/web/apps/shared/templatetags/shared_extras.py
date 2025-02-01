from django import template
from django.templatetags.static import static
from django.conf import settings

register = template.Library()

language_icons = (
    ("az", static("base/img/lang/azerbaijan.webp")),
    ("en", static("base/img/lang/english.png")),
)
    

@register.filter
def get_language_icon(value: str) -> str:
    return dict(language_icons).get(value, "")


@register.simple_tag(takes_context=True)
def build_language_path(context, path: str, language: str, current_language: str) -> str:
    prefix = f"/{current_language}/"
    if current_language in (item[0] for item in settings.LANGUAGES):
        newPrefix = f"/{language}/"
        if prefix in path and language != settings.LANGUAGE_CODE:
            return path.replace(prefix, newPrefix)
        elif prefix not in path and language is not settings.LANGUAGE_CODE:
            return newPrefix.rstrip("/")+path
        elif (prefix in path and language is settings.LANGUAGE_CODE) or (language is not settings.LANGUAGE_CODE):
            return f"/{path.replace(prefix, '')}"
    return path
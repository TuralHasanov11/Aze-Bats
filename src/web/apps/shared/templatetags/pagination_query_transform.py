from django import template
from django.http import HttpRequest

register = template.Library()

@register.simple_tag(takes_context=True)
def pagination_query_transform(context, **kwargs):
    request: HttpRequest = context["request"]
    query = request.GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()
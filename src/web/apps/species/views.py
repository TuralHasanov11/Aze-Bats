from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.utils.translation import get_language

from apps.species.models import Bat


import logging

logger = logging.getLogger(__name__)


class BatListView(View):
    http_method_names = ["get"]
    paginate_by = 10

    def get(self, request: HttpRequest) -> HttpResponse:
        page = int(request.GET.get("page", 1))
        bats = Paginator(
            Bat.entries.list(language=get_language()), self.paginate_by
        ).get_page(page)

        return render(request, "bats/list.html", {"bats": bats})


class BatDetailView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        bat = Bat.entries.get_by_slug(slug=slug, language=get_language())

        if not bat:
            logger.error("Bat with slug %s not found", slug)
            return HttpResponseNotFound()

        return render(request, "bats/detail.html", {"bat": bat})

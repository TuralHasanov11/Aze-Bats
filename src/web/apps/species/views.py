import logging

from apps.shared.utils import BreadcrumbMenu
from apps.species.models import Bat
from apps.species.specifications import (
    GetBatBySlugSpecification,
)
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views import View

logger = logging.getLogger(__name__)


class BatListView(View):
    http_method_names = ["get"]
    paginate_by = 24

    def get(self, request: HttpRequest) -> HttpResponse:
        page = int(request.GET.get("page", 1))
        bats = Paginator(Bat.entries.list(), self.paginate_by).get_page(page)
        
        breadcrumb_menu: BreadcrumbMenu = [
            {"name": _("Home"), "url": reverse("apps.home:home")},
            {"name": _("Species"), "url": reverse("apps.species:list")},
        ]

        return render(request, "species/list.html", {"bats": bats, "breadcrumb_menu": breadcrumb_menu})


class BatDetailView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        bat = Bat.entries.single(GetBatBySlugSpecification(slug, get_language()))

        if not bat:
            logger.error("Bat with slug %s not found", slug)
            return HttpResponseNotFound()
        
        breadcrumb_menu: BreadcrumbMenu = [
            {"name": _("Home"), "url": reverse("apps.home:home")},
            {"name": _("Species"), "url": reverse("apps.species:list")},
            {"name": bat.name, "url": bat.get_absolute_url()},
        ]

        return render(request, "species/detail.html", {"bat": bat, "breadcrumb_menu": breadcrumb_menu})

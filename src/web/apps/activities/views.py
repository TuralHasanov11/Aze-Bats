from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from django.utils.translation import get_language
from apps.activities.models import Project, SiteVisit
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)


class ProjectListView(View):
    http_method_names = ["get"]
    paginate_by = 10

    def get(self, request: HttpRequest) -> HttpResponse:
        page = int(request.GET.get("page", 1))
        projects = Paginator(
            Project.entries.list(language=get_language()), self.paginate_by
        ).get_page(page)
        return render(request, "activities/projects/list.html", {"projects": projects})


class ProjectDetailView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        project = Project.entries.get_by_slug(slug=slug)

        if not project:
            logger.error("Project with slug %s not found", slug)
            return HttpResponseNotFound()

        return render(request, "activities/projects/detail.html", {"project": project})


class SiteVisitListView(View):
    http_method_names = ["get"]
    paginate_by = 10

    def get(self, request: HttpRequest) -> HttpResponse:
        page = int(request.GET.get("page", 1))
        site_visits = Paginator(
            SiteVisit.entries.list(language=get_language()), self.paginate_by
        ).get_page(page)
        return render(
            request, "activities/site_visits/list.html", {"site_visits": site_visits}
        )


class SiteVisitDetailView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        site_visit = SiteVisit.entries.get_by_slug(slug=slug)

        if not site_visit:
            logger.error("Site Visit with slug %s not found", slug)
            return HttpResponseNotFound()

        return render(
            request, "activities/site_visits/detail.html", {"site_visit": site_visit}
        )

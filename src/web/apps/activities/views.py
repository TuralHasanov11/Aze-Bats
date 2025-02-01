from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from apps.activities.models import Project, SiteVisit
from django.core.paginator import Paginator
import logging

from apps.activities.specifications import (
    GetProjectBySlugSpecification,
    GetProjectsSpecification,
    GetSiteVisitBySlugSpecification,
    GetSiteVisitsSpecification,
)

logger = logging.getLogger(__name__)


class ProjectListView(View):
    http_method_names = ["get"]
    paginate_by = 10

    def get(self, request: HttpRequest) -> HttpResponse:
        page = int(request.GET.get("page", 1))
        projects = Paginator(Project.entries.list(), self.paginate_by).get_page(page)
        return render(request, "activities/projects/list.html", {"projects": projects})


class ProjectDetailView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        project = Project.entries.single(GetProjectBySlugSpecification(slug))

        if not project:
            logger.error("Project with slug %s not found", slug)
            return HttpResponseNotFound()

        recent_projects = Project.entries.list(
            GetProjectsSpecification().except_by_id(project.pk)
        )[:3]

        return render(
            request,
            "activities/projects/detail.html",
            {"project": project, "recent_projects": recent_projects},
        )


class SiteVisitListView(View):
    http_method_names = ["get"]
    paginate_by = 10

    def get(self, request: HttpRequest) -> HttpResponse:
        page = int(request.GET.get("page", 1))
        site_visits = Paginator(SiteVisit.entries.list(), self.paginate_by).get_page(
            page
        )
        return render(
            request, "activities/site_visits/list.html", {"site_visits": site_visits}
        )


class SiteVisitDetailView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        site_visit = SiteVisit.entries.single(GetSiteVisitBySlugSpecification(slug))

        if not site_visit:
            logger.error("Site Visit with slug %s not found", slug)
            return HttpResponseNotFound()

        recent_site_visits = SiteVisit.entries.list(
            GetSiteVisitsSpecification().except_by_id(site_visit.pk)
        )[:3]

        return render(
            request,
            "activities/site_visits/detail.html",
            {"site_visit": site_visit, "recent_site_visits": recent_site_visits},
        )

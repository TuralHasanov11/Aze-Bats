from dataclasses import dataclass
from typing import Iterable, List
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from apps.shared.utils import BreadcrumbMenu
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.activities.models import Project, SiteVisit
from apps.articles.models import Article
from apps.home.forms import SearchForm
from apps.species.models import Bat
from apps.species.specifications import SearchBatsSpecification
from apps.activities.specifications import (
    SearchProjectsSpecification,
    SearchSiteVisitsSpecification,
)
from apps.home.models import CarouselItem


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        site_visits = SiteVisit.entries.list()[:3]
        projects = Project.entries.list()[:3]
        articles = Article.entries.list()[:3]
        carousel_items = CarouselItem.objects.all()

        return render(
            request,
            "home/home.html",
            {"site_visits": site_visits, "projects": projects, "articles": articles, "carousel_items": carousel_items},
        )


class AboutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        breadcrumb_menu: BreadcrumbMenu = [
            {"name": _("Home"), "url": reverse("apps.home:home")},
            {"name": _("About Us"), "url": reverse("apps.home:about")},
        ]

        return render(request, "home/about.html", {"breadcrumb_menu": breadcrumb_menu})


class PrivacyPolicyView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        breadcrumb_menu: BreadcrumbMenu = [
            {"name": _("Home"), "url": reverse("apps.home:home")},
            {"name": _("Privacy Policy"), "url": reverse("apps.home:privacy-policy")},
        ]

        return render(
            request, "home/privacy_policy.html", {"breadcrumb_menu": breadcrumb_menu}
        )


class SearchView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = SearchForm(request.GET)

        if form.is_valid():
            search: str = form.cleaned_data["search"]
            bats = Bat.entries.list(SearchBatsSpecification(search=search))[:10]
            site_visits = SiteVisit.entries.list(
                SearchSiteVisitsSpecification(search=search)
            )[:10]
            projects = Project.entries.list(SearchProjectsSpecification(search=search))[
                :10
            ]

            return render(
                request,
                "home/search.html",
                {"bats": bats, "site_visits": site_visits, "projects": projects},
            )

        return render(request, "home/search.html")

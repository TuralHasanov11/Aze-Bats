from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from apps.shared.utils import BreadcrumbMenu
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "home/home.html")


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

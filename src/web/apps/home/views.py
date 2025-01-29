from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "home/home.html")


class AboutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "home/about.html")


class ContactView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "home/contact.html")


class PrivacyPolicyView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "home/privacy_policy.html")

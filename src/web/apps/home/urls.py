from django.urls import path

from apps.home import views


app_name = "apps.home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("privacy-policy/", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
]

from django.urls import path

from apps.home import views


app_name = "apps.home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("privacy-policy/", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
]

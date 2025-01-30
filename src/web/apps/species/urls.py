from apps.species import views
from django.urls import path

app_name = "apps.bats"

urlpatterns = [
    path("", views.BatListView.as_view(), name="list"),
    path("<str:slug>", views.BatDetailView.as_view(), name="detail"),
]

from apps.activities import views
from django.urls import path

app_name = "apps.activities"

urlpatterns = [
    path("projects", views.ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<str:slug>", views.ProjectDetailView.as_view(), name="project-detail"
    ),
    path("field-trips", views.SiteVisitListView.as_view(), name="field-trip-list"),
    path(
        "field-trips/<str:slug>",
        views.SiteVisitDetailView.as_view(),
        name="field-trip-detail",
    ),
]

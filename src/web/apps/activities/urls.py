from activities import views
from django.urls import path

app_name = "apps.activities"

urlpatterns = [
    path("projects", views.ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<str:slug>", views.ProjectDetailView.as_view(), name="project-detail"
    ),
    path("site-visits", views.SiteVisitListView.as_view(), name="site-visit-list"),
    path(
        "site-visits/<str:slug>",
        views.SiteVisitDetailView.as_view(),
        name="site-visit-detail",
    ),
]

from apps.articles import views
from django.urls import path

app_name = "apps.articles"

urlpatterns = [
    path("articles", views.ArticleListView.as_view(), name="article-list"),
]

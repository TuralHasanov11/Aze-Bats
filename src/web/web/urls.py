from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from apps.species import sitemap as bats_sitemap
from apps.activities import sitemap as activities_sitemap
from apps.articles import sitemap as articles_sitemap
from apps.home import sitemap as home_sitemap

sitemaps = {
    "bats": bats_sitemap.BatSiteMap,
    "projects": activities_sitemap.ProjectSiteMap,
    "visits": activities_sitemap.SiteVisitSiteMap,
    "articles": articles_sitemap.ArticleSiteMap,
    'home': home_sitemap.StaticViewSitemap,
}

urlpatterns = i18n_patterns(
    path("", include("apps.home.urls", namespace="apps.home")),
    path("species/", include("apps.species.urls", namespace="apps.species")),
    path("activities/", include("apps.activities.urls", namespace="apps.activities")),
    path("articles/", include("apps.articles.urls", namespace="apps.articles")),
    prefix_default_language=False,
)

urlpatterns += [
    path('admin/', admin.site.urls),
    path("logs/", include("log_viewer.urls")),
    path('tinymce/', include('tinymce.urls')),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    re_path(r"^languages/", include("rosetta.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
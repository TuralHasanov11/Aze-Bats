from apps.activities.models import Project, SiteVisit
from django.contrib.sitemaps import Sitemap


class ProjectSiteMap(Sitemap):
    i18n = True
    changefreq = "weekly"

    def items(self):
        return Project.entries.list()

    def lastmod(self, obj: Project):
        return obj.updated_at


class SiteVisitSiteMap(Sitemap):
    i18n = True
    changefreq = "weekly"

    def items(self):
        return SiteVisit.entries.list()

    def lastmod(self, obj: SiteVisit):
        return obj.updated_at

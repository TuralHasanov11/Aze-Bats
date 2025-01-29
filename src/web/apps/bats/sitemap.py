from apps.bats.models import Bat
from django.contrib.sitemaps import Sitemap


class BatSiteMap(Sitemap):
    changefreq = "weekly"
    i18n = True

    def items(self):
        return Bat.entries.list()

    def lastmod(self, obj: Bat):
        return obj.updated_at


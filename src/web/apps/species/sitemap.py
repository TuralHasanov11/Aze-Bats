from apps.species.models import Bat, Family, Genus
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.species.specifications import GetGenusesWithFamilySpecification

class BatSiteMap(Sitemap):
    changefreq = "weekly"
    i18n = True

    def items(self):
        return Bat.entries.list()

    def lastmod(self, obj: Bat):
        return obj.updated_at

class FamilySiteMap(Sitemap):
    changefreq = "weekly"
    i18n = True

    def items(self):
        return Family.entries.list()

    def lastmod(self, obj: Family):
        return obj.updated_at
    
    def location(self, obj: Family):
        return reverse("apps.species:list") + f"?family={obj.slug}",
    
    
class GenusSiteMap(Sitemap):
    changefreq = "weekly"
    i18n = True

    def items(self):
        return GetGenusesWithFamilySpecification().handle(Genus.entries.list())

    def lastmod(self, obj: Genus):
        return obj.updated_at
    
    def location(self, obj: Genus):
        return reverse("apps.species:list") + f"?family={obj.family.slug}&genus={obj.slug}",

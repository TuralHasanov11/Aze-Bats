from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    i18n = True
    
    def items(self):
        return [
            "home:home",
            "home:about",
            "home:contact",
            "home:privacy-policy",
        ]

    def location(self, item):
        return reverse(item)
from apps.articles.models import Article
from django.contrib.sitemaps import Sitemap


class ArticleSiteMap(Sitemap):
    changefreq = "weekly"
    i18n = True

    def items(self):
        return Article.entries.list()

    def lastmod(self, obj: Article):
        return obj.updated_at

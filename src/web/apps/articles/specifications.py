

from typing import Optional

from apps.articles.models import Article
from django.db.models.query import QuerySet

from apps.shared.specification import Specification


class SearchArticlesSpecification(Specification):
    search: Optional[str]

    def __init__(self, search: str):
        self.search = search

    def handle(self, queryset: QuerySet[Article]) -> QuerySet[Article]:
        if self.search:
            queryset = queryset.filter(name__icontains=self.search)
        return super().handle(queryset)
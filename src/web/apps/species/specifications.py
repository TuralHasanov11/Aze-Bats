from typing import Optional
from apps.species.models import Bat, BatAttribute
from apps.shared.specification import Specification
from django.db.models import QuerySet, Prefetch


class GetBatBySlugSpecification(Specification[Bat]):
    slug: str
    language: str

    def __init__(self, slug: str, language: str):
        self.slug = slug
        self.language = language

    def handle(self, queryset: QuerySet[Bat]) -> QuerySet[Bat]:
        return queryset.prefetch_related(
            "images",
            Prefetch(
                "attributes", queryset=BatAttribute.objects.filter(language=self.language)
            ),
        ).filter(slug=self.slug)


class SearchBatsSpecification(Specification[Bat]):
    search: Optional[str]

    def __init__(self, search: Optional[str]):
        self.search = search

    def handle(self, queryset: QuerySet[Bat]) -> QuerySet[Bat]:
        if self.search:
            queryset = queryset.filter(name__icontains=self.search)
        return super().handle(queryset)

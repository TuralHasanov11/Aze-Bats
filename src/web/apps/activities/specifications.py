from typing import Optional

from apps.activities.models import Project, SiteVisit
from apps.shared.specification import Specification
from django.db.models import QuerySet


class SearchSiteVisitsSpecification(Specification):
    search: Optional[str]

    def __init__(self, search: str):
        self.search = search

    def handle(self, queryset: QuerySet[SiteVisit]) -> QuerySet[SiteVisit]:
        if self.search:
            queryset = queryset.filter(name__icontains=self.search)
        return super().handle(queryset)


class GetSiteVisitsSpecification(Specification):
    except_id: Optional[int]
    
    def __init__(self):
        pass

    def handle(self, queryset: QuerySet[SiteVisit]) -> QuerySet[SiteVisit]:
        return super().handle(queryset)
    
    def except_by_id(self, except_id: int):
        self.except_id = except_id
        return self
    
class GetSiteVisitBySlugSpecification(Specification):
    slug: str
    
    def __init__(self, slug: str):
        self.slug = slug
        
    def handle(self, queryset: QuerySet[SiteVisit]) -> QuerySet[SiteVisit]:
        return queryset.filter(slug=self.slug)


class SearchProjectsSpecification(Specification):
    search: Optional[str]

    def __init__(self, search: str):
        self.search = search

    def handle(self, queryset: QuerySet[SiteVisit]) -> QuerySet[SiteVisit]:
        if self.search:
            queryset = queryset.filter(name__icontains=self.search)
        return super().handle(queryset)

class GetProjectsSpecification(Specification):
    except_id: Optional[int]


    def __init__(self):
        pass

    def handle(self, queryset: QuerySet[Project]) -> QuerySet[Project]:
        return super().handle(queryset)
    
    def except_by_id(self, except_id: int):
        self.except_id = except_id
        return self

class GetProjectsByLanguageSpecification(Specification):
    language: Optional[str]

    def __init__(self, language: Optional[str]):
        self.language = language

    def handle(self, queryset: QuerySet[Project]) -> QuerySet[Project]:
        if self.language:
            queryset = queryset.filter(language=self.language)
        return super().handle(queryset)

class GetProjectBySlugSpecification(Specification):
    slug: str
    
    def __init__(self, slug: str):
        self.slug = slug
        
    def handle(self, queryset: QuerySet[Project]) -> QuerySet[Project]:
        return queryset.filter(slug=self.slug)
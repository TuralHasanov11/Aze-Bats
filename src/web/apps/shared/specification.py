from __future__ import annotations
from abc import ABC
from typing import Optional, TypeVar, Generic
from django.db.models.query import QuerySet
from django.db.models import Model  


TModel = TypeVar('TModel', bound=Model)

class Specification(ABC, Generic[TModel]):
    next: Optional[Specification[TModel]] = None

    def set_next(self, filter: Specification[TModel]):
        self.next = filter
        return filter

    def handle(self, queryset: QuerySet[TModel]) -> QuerySet[TModel]:
        if self.next:
            return self.next.handle(queryset)
        return queryset
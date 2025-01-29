from abc import ABC
from dataclasses import dataclass, asdict
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Model
from typing import TypeVar, Dict

TModel = TypeVar('TModel', bound=Model)

class Specification[TModel](ABC):
    criteria: Dict[str, Any]
    criteria_condition: bool

    def __init__(self, criteria: Dict, criteria_condition: bool = True):
        self.criteria = criteria
        self.criteria_condition = criteria_condition


class SpecificationEvaluator:
    
    @staticmethod
    def filter(
        queryable: QuerySet[TModel], specification: Specification
    ) -> QuerySet[TModel]:
        return (
            queryable.filter(**specification.criteria)
            if specification.criteria_condition
            else queryable
        )

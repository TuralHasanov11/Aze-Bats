from typing import Dict, Optional, Any
from apps.bats.models import Bat
from apps.shared.specification import Specification


class GetBatSpecification(Specification[Bat]):
    def __init__(self, slug: str, language: str):
        super().__init__({"slug": slug, "language": language})


class GetBatsSpecification(Specification[Bat]):
    def __init__(self, language: str, genus_id: Optional[int] = None):
        criteria: Dict[str, Any] = {
            "language": language,
        }

        if genus_id:
            criteria["genus_id"] = genus_id

        super().__init__(criteria)

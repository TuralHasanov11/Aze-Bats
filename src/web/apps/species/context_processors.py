

from typing import Dict
from django.http import HttpRequest

from apps.species.models import Family, Genus, Bat


def families(request: HttpRequest) -> Dict:
    families = Family.entries.list()
    return {
        'families': families,
        "family_count": len(families),
    }
    
def genus_count(request: HttpRequest) -> Dict:
    return {
        "genus_count": Genus.entries.count(),
    }
    
def bat_count(request: HttpRequest) -> Dict:
    return {
        "bat_count": Bat.entries.count(),
    }
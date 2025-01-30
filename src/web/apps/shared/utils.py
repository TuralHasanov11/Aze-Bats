from typing import List, TypedDict

class BreadcrumbItem(TypedDict):
    name: str
    url: str
    
BreadcrumbMenu = List[BreadcrumbItem]
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from apps.home.forms import SearchForm
from apps.species.models import Family
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from apps.home.author import load_author_data




def home_context(request: HttpRequest) -> Dict:
    author = load_author_data(get_language())
    return {"app_name": settings.APP_NAME, "author": author}


@dataclass
class MenuItem:
    name: str
    route: str
    submenu: Optional[List["MenuItem"]] = field(default_factory=list)


# Define the menu items


def base_menu(request: HttpRequest) -> Dict[str, List[MenuItem]]:
    families = Family.entries.list_with_genuses()
    family_menu_items: List[MenuItem] = [
        MenuItem(
            name=_("All"),
            route=reverse("apps.species:list"),
        )
    ]

    for family in families:
        if family.genus_list:
            family_menu_items.append(
                MenuItem(
                    name=family.name,
                    route=reverse("apps.species:list") + f"?family={family.slug}",
                    submenu=[
                        MenuItem(
                            name=_("All"),
                            route=reverse("apps.species:list")
                            + f"?family={family.slug}",
                        )
                    ]
                    + [
                        MenuItem(
                            name=genus.name,
                            route=reverse("apps.species:list")
                            + f"?family={family.slug}&genus={genus.slug}",
                        )
                        for genus in family.genus_list
                    ],
                )
            )
        else:
            family_menu_items.append(
                MenuItem(
                    name=family.name,
                    route=reverse("apps.species:list") + f"?family={family.slug}",
                )
            )

    menu = [
        MenuItem(name=_("Home"), route=reverse("apps.home:home")),
        MenuItem(name=_("About Us"), route=reverse("apps.home:about")),
        MenuItem(
            name=_("Activities"),
            route="#",
            submenu=[
                MenuItem(
                    name=_("Site Visits"),
                    route=reverse("apps.activities:site-visit-list"),
                ),
                MenuItem(
                    name=_("Projects"), route=reverse("apps.activities:project-list")
                ),
            ],
        ),
        MenuItem(
            name=_("Bats"),
            route=reverse("apps.species:list"),
            submenu=family_menu_items,
        ),
    ]

    return {
        "base_menu": menu,
    }


def search_form(request: HttpRequest) -> Dict:
    return {"search_form": SearchForm(request.GET)}

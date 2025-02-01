from dataclasses import dataclass, field
from typing import Collection, Dict, List, Optional

from django.conf import settings
from django.http import HttpRequest
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.species.models import Family
from apps.home.forms import SearchForm

@dataclass
class SocialLink:
    name: str
    url: str
    icon: str


@dataclass
class Contact:
    email: str


@dataclass
class Author:
    name: str
    specialty: str
    profile_image: str
    bio: Optional[str]
    social_links: Collection[SocialLink]
    contact: Contact


def home_context(request: HttpRequest) -> Dict:
    author = Author(
        name="John Doe",
        specialty="Software Engineer",
        profile_image=static("base/img/authority/01.jpg"),
        bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        social_links=[
            SocialLink(
                name="YouTube", url="https://youtube.com", icon="fab fa-youtube"
            ),
            SocialLink(
                name="Twitter", url="https://twitter.com", icon="fab fa-twitter"
            ),
            SocialLink(
                name="LinkedIn", url="https://linkedin.com", icon="fab fa-linkedin-in"
            ),
            SocialLink(
                name="Facebook", url="https://facebook.com", icon="fab fa-facebook-f"
            ),
        ],
        contact=Contact(email="test@test.com"),
    )

    return {"app_name": settings.APP_NAME, "author": author}


@dataclass
class MenuItem:
    name: str
    route: str
    submenu: Optional[List["MenuItem"]] = field(default_factory=list)


# Define the menu items


def base_menu(request: HttpRequest) -> Dict[str, List[MenuItem]]:
    families = Family.entries.list_with_genuses()
    family_menu_items: List[MenuItem] = []
    
    for family in families:
        if family.genus_list:
            family_menu_items.append(
                MenuItem(
                    name=family.name,
                    route=reverse('apps.species:list') + f"?family={family.slug}",
                    submenu=[
                        MenuItem(
                            name=genus.name,
                            route=reverse('apps.species:list') + f"?family={family.slug}&genus={genus.slug}",
                        )
                        for genus in family.genus_list
                    ],
                )
            )
        else:
            family_menu_items.append(
                MenuItem(
                    name=family.name,
                    route=reverse('apps.species:list') + f"?family={family.slug}",
                )
            )
    
    menu = [
        MenuItem(name=_("Home"), route=reverse('apps.home:home')),
        MenuItem(name=_("About Us"), route=reverse('apps.home:about')),
        MenuItem(name=_("Activities"), route="#", submenu=[
            MenuItem(name=_("Site Visits"), route=reverse('apps.activities:site-visit-list')),
            MenuItem(name=_("Projects"), route=reverse('apps.activities:project-list')),
        ]),
        MenuItem(name= _("Bats"), route=reverse('apps.species:list'), submenu=family_menu_items),
    ]
    
    return {
        "base_menu": menu,
    }
    
    
def search_form(request: HttpRequest) -> Dict:
    return {"search_form": SearchForm(request.GET)}
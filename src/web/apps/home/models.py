from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Collection, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce import models as tinymce_models

from apps.shared.models import LanguageField

    
class CarouselItem(models.Model):
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='carousel/')
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class StaticTextKey(Enum):
    ABOUT = "about"
    PRIVACY_POLICY = "privacy_policy"

    @classmethod
    def choices(cls):
        return [(key.value, _(key.name.replace("_", " ").title())) for key in cls]


class StaticTextManager(models.Manager):
    def single(self, key, language="en") -> Optional[StaticText]:
        return self.filter(key=key, language=language).first()


class StaticText(models.Model):
    key = models.CharField(max_length=50, choices=StaticTextKey.choices())
    language = LanguageField()
    content = tinymce_models.HTMLField()
    
    entries = StaticTextManager()

    def __str__(self):
        return f"{self.key} ({self.language})"


@dataclass
class SocialLink:
    name: str
    url: str
    icon: str


@dataclass
class Author:
    name: str
    specialty: str
    profile_image: str
    bio: Optional[str]
    social_links: Collection[SocialLink]
    email: str
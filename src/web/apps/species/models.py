from __future__ import annotations
from typing import Collection, Optional
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import (
    LanguageField,
    NameField,
    SlugField,
)
import uuid

from apps.shared.specification import Specification
from tinymce import models as tinymce_models


class FamilyManager(models.Manager):
    def get_by_slug(self, slug: str) -> Optional[Family]:
        return self.get_queryset().filter(slug=slug).first()

    def list(self) -> models.QuerySet[Family]:
        return self.get_queryset().all()
    
    def list_with_genuses(self) -> models.QuerySet[Family]:
        return self.get_queryset().prefetch_related("genuses")


class Family(models.Model):
    name = NameField(unique=True)
    slug = SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entries = FamilyManager()

    class Meta:
        verbose_name_plural = _("Families")
        verbose_name = _("Family")
        ordering = ("name",)

    def __str__(self):
        return self.name
    
    @property 
    def genus_list(self) -> Collection[Genus]:
        if not hasattr(self, "genuses"):
            return []
        return getattr(self, "genuses").all()


class GenusManager(models.Manager):
    def get_by_slug(self, slug: str, language: str) -> Optional[Genus]:
        return self.get_queryset().filter(slug=slug).first()

    def list(self, language: str) -> models.QuerySet[Genus]:
        return self.get_queryset().all()


class Genus(models.Model):
    name = NameField(unique=True)
    slug = SlugField()
    family = models.ForeignKey(Family, related_name="genuses", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entries = GenusManager()

    class Meta:
        verbose_name_plural = _("Genus")
        verbose_name = _("Genus")
        ordering = ("name",)

    def __str__(self):
        return self.name
    
    @property
    def bat_list(self) -> Collection[Bat]:
        if not hasattr(self, "bats"):
            return []
        return getattr(self, "bats").all()
    

class BatManager(models.Manager):
    def list(self, specification: Optional[Specification[Bat]] = None) -> models.QuerySet[Bat]:
        if specification:
            return specification.handle(self.get_queryset())
        return self.get_queryset().all()
    
    def single(self, specification: Optional[Specification[Bat]] = None) -> Optional[Bat]:
        if specification:
            return specification.handle(self.get_queryset()).first()
        return self.get_queryset().first()

def upload_bat_cover_image_to_func(instance: models.Model, filename: str) -> str:
    return f"bats/{instance.pk}/{uuid.uuid4()}-{filename}"

class Bat(models.Model):
    name = NameField(unique=True)
    slug = SlugField()
    cover_image = models.ImageField(upload_to=upload_bat_cover_image_to_func, verbose_name=_("Cover Image"))
    genus = models.ForeignKey(Genus, related_name="bats", on_delete=models.CASCADE)
    is_in_red_list = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entries = BatManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("apps.species:detail", kwargs={"slug": self.slug})
    
    @property
    def attribute(self) -> Optional[BatAttribute]:
        if not hasattr(self, "attributes"):
            return None
        return getattr(self, "attributes").first()


class BatAttribute(models.Model):
    bat = models.ForeignKey(Bat, related_name="attributes", on_delete=models.CASCADE)
    description = tinymce_models.HTMLField()
    language = LanguageField()

def upload_bat_image_to_func(instance: models.Model, filename: str) -> str:
    return f"bats/{getattr(instance, "bat_id")}/{uuid.uuid4()}-{filename}"

class BatImage(models.Model):
    bat = models.ForeignKey(Bat, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=upload_bat_image_to_func, verbose_name=_("Cover Image"))

    def __str__(self):
        return self.image.url

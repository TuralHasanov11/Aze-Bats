from __future__ import annotations
from typing import Collection, Optional
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.shared.models import (
    LanguageField,
    NameField,
    SlugField,
)
import uuid

from apps.shared.specification import Specification
from tinymce import models as tinymce_models


class FamilyManager(models.Manager):
    def list(self, specification: Optional[Specification[Family]] = None) -> models.QuerySet[Family]:
        if specification:
            return specification.handle(self.get_queryset())
        return self.get_queryset().all()
    
    def single(self, specification: Optional[Specification[Family]] = None) -> Optional[Family]:
        if specification:
            return specification.handle(self.get_queryset()).first()
        return self.get_queryset().first()


class Family(models.Model):
    name = NameField(unique=True)
    slug = SlugField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update Date"))

    entries = FamilyManager()

    class Meta:
        verbose_name_plural = _("Families")
        verbose_name = _("Family")
        ordering = ("name",)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property 
    def genus_list(self) -> Collection[Genus]:
        if not hasattr(self, "genuses"):
            return []
        return getattr(self, "genuses").all()


class GenusManager(models.Manager):
    def list(self, specification: Optional[Specification[Genus]] = None) -> models.QuerySet[Genus]:
        if specification:
            return specification.handle(self.get_queryset())
        return self.get_queryset().all()
    
    def single(self, specification: Optional[Specification[Genus]] = None) -> Optional[Genus]:
        if specification:
            return specification.handle(self.get_queryset()).first()
        return self.get_queryset().first()


class Genus(models.Model):
    name = NameField(unique=True)
    slug = SlugField()
    family = models.ForeignKey(Family, related_name="genuses", on_delete=models.CASCADE, verbose_name=_("Family"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update Date"))

    entries = GenusManager()

    class Meta:
        verbose_name_plural = _("Genus")
        verbose_name = _("Genus")
        ordering = ("name",)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
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
    if isinstance(instance, Bat):
        return f"bats/{instance.slug}/{uuid.uuid4()}-{filename}"
    raise ValueError("Invalid instance type for upload_bat_cover_image_to_func")

class Bat(models.Model):
    name = NameField(unique=True)
    slug = SlugField()
    cover_image = models.ImageField(upload_to=upload_bat_cover_image_to_func, verbose_name=_("Cover Image"))
    genus = models.ForeignKey(Genus, related_name="bats", on_delete=models.CASCADE, verbose_name=_("Genus"))
    is_in_red_list = models.BooleanField(default=False, blank=True, verbose_name=_("Is in Red List"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update Date"))

    entries = BatManager()

    class Meta:
        ordering = ("name",)
        verbose_name = _("Bat")
        verbose_name_plural = _("Bats")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("apps.species:detail", kwargs={"slug": self.slug})
    
    @property
    def attribute(self) -> Optional[BatAttribute]:
        if not hasattr(self, "attributes"):
            return None
        return getattr(self, "attributes").first()


class BatAttribute(models.Model):
    bat = models.ForeignKey(Bat, related_name="attributes", on_delete=models.CASCADE, verbose_name=_("Bat"))
    description = tinymce_models.HTMLField(verbose_name=_("Description"))
    language = LanguageField()
    
    class Meta:
        verbose_name = _("Bat Attribute")
        verbose_name_plural = _("Bat Attributes")

def upload_bat_image_to_func(instance: models.Model, filename: str) -> str:
    if isinstance(instance, BatImage):
        return f"bats/{instance.bat.slug}/{uuid.uuid4()}-{filename}"
    raise ValueError("Invalid instance type for upload_bat_image_to_func")

class BatImage(models.Model):
    bat = models.ForeignKey(Bat, on_delete=models.CASCADE, related_name="images", verbose_name=_("Bat"))
    image = models.ImageField(upload_to=upload_bat_image_to_func, verbose_name=_("Cover Image"))

    def __str__(self):
        return self.image.url
    
    class Meta:
        verbose_name = _("Bat Image")
        verbose_name_plural = _("Bat Images")

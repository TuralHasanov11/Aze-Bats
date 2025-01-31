from __future__ import annotations
from typing import Optional
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import (
    LanguageField,
    NameField,
    RichTextField,
    SlugField,
)
import uuid


class FamilyManager(models.Manager):
    def get_by_slug(self, slug: str, language: str) -> Optional[Family]:
        return self.get_queryset().filter(slug=slug).first()

    def list(self, language: str) -> models.QuerySet[Family]:
        return self.get_queryset().all()


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


class BatManager(models.Manager):
    def get_by_slug(self, slug: str, language: str) -> Optional[Bat]:
        return self.get_queryset().filter(slug=slug).first()

    def list(self, language: Optional[str] = "") -> models.QuerySet[Bat]:
        return self.get_queryset().all()


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
        return reverse("species:detail", kwargs={"slug": self.slug})


class BatAttributes(models.Model):
    bat = models.ForeignKey(Bat, related_name="attributes", on_delete=models.CASCADE)
    description = RichTextField()
    language = LanguageField()

def upload_bat_image_to_func(instance: models.Model, filename: str) -> str:
    return f"bats/{getattr(instance, "bat_id")}/{uuid.uuid4()}-{filename}"

class BatImage(models.Model):
    bat = models.ForeignKey(Bat, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=upload_bat_image_to_func, verbose_name=_("Cover Image"))

    def __str__(self):
        return self.image.url

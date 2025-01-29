from __future__ import annotations
from typing import Optional
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import (
    ImageField,
    LanguageField,
    NameField,
    RichTextField,
    SlugField,
)
from apps.shared.helpers import generate_slug


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

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.name)
        return super().save(*args, **kwargs)


class GenusManager(models.Manager):
    def get_by_slug(self, slug: str, language: str) -> Optional[Genus]:
        return self.get_queryset().filter(slug=slug).first()

    def list(self, language: str) -> models.QuerySet[Genus]:
        return self.get_queryset().all()


class Genus(models.Model):
    name = NameField(unique=True)
    slug = SlugField()
    family = models.ForeignKey(Family, related_name="family", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entries = GenusManager()

    class Meta:
        verbose_name_plural = _("Genus")
        verbose_name = _("Genus")
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.name)
        return super().save(*args, **kwargs)


class BatManager(models.Manager):
    def get_by_slug(self, slug: str, language: str) -> Optional[Bat]:
        return self.get_queryset().filter(slug=slug).first()

    def list(self, language: str) -> models.QuerySet[Bat]:
        return self.get_queryset().all()


class Bat(models.Model):
    name = NameField(unique=True)
    slug = SlugField()
    cover_image = ImageField("bats", _("Cover Image"))
    genus = models.ForeignKey(Genus, related_name="genus", on_delete=models.CASCADE)
    is_in_red_book = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entries = BatManager()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("species:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.name)
        return super().save(*args, **kwargs)


class BatAttributes(models.Model):
    bat = models.ForeignKey(Bat, related_name="attributes", on_delete=models.CASCADE)
    description = RichTextField()
    language = LanguageField()


class BatImage(models.Model):
    bat = models.ForeignKey(Bat, on_delete=models.CASCADE, related_name="images")
    image = ImageField("bats", _("Image"))

    def __str__(self):
        return self.image.url

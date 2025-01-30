from __future__ import annotations
from typing import Optional
from django.db import models
from django.urls import reverse
from apps.shared.models import (
    ImageField,
    LanguageField,
    NameField,
    RichTextField,
    SlugField,
)
from django.utils.translation import gettext_lazy as _


class ProjectManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()

    def get_by_slug(self, slug: str) -> Optional[Project]:
        return self.get_queryset().filter(slug=slug).first()

    def list(self, language: Optional[str] = '') -> models.QuerySet[Project]:
        return self.get_queryset().all()


class Project(models.Model):
    name = NameField()
    slug = SlugField()
    cover_image = ImageField("projects", _("Cover Image"))
    description = RichTextField()
    language = LanguageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    entries = ProjectManager()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("apps.activities:project-detail", kwargs={"slug": self.slug})


class SiteVisitManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()

    def get_by_slug(self, slug: str) -> Optional[SiteVisit]:
        return self.get_queryset().filter(slug=slug).first()

    def list(self, language: Optional[str] = '') -> models.QuerySet[SiteVisit]:
        return self.get_queryset().all()


class SiteVisit(models.Model):
    name = NameField()
    slug = SlugField()
    cover_image = ImageField("site_visits", _("Cover Image"))
    description = RichTextField()
    language = LanguageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    entries = SiteVisitManager()

    class Meta:
        verbose_name = _("Site Visit")
        verbose_name_plural = _("Site Visits")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("apps.activities:site-visit-detail", kwargs={"slug": self.slug})

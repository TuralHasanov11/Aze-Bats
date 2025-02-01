from __future__ import annotations

import uuid
from typing import Optional

from apps.shared.models import (
    LanguageField,
    NameField,
    RichTextField,
    SlugField,
)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.shared.specification import Specification


class ProjectManager(models.Manager):
    def list(self, specification: Optional[Specification[Project]] = None) -> models.QuerySet[Project]:
        if specification:
            return specification.handle(self.get_queryset())
        return self.get_queryset().all()
    
    def single(self, specification: Optional[Specification[Project]] = None) -> Optional[Project]:
        if specification:
            return specification.handle(self.get_queryset()).first()
        return self.get_queryset().first()


def upload_project_cover_image_to_func(instance: models.Model, filename: str) -> str:
    return f"projects/{instance.pk}/{uuid.uuid4()}-{filename}"


class Project(models.Model):
    name = NameField()
    slug = SlugField()
    cover_image = models.ImageField(
        upload_to=upload_project_cover_image_to_func, verbose_name=_("Cover Image")
    )
    description = RichTextField()
    language = LanguageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entries = ProjectManager()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("apps.activities:project-detail", kwargs={"slug": self.slug})


class SiteVisitManager(models.Manager):
    def list(self, specification: Optional[Specification[SiteVisit]] = None) -> models.QuerySet[SiteVisit]:
        if specification:
            return specification.handle(self.get_queryset())
        return self.get_queryset().all()
    
    def single(self, specification: Optional[Specification[SiteVisit]] = None) -> Optional[SiteVisit]:
        if specification:
            return specification.handle(self.get_queryset()).first()
        return self.get_queryset().first()


def upload_site_visit_cover_image_to_func(instance: models.Model, filename: str) -> str:
    return f"site_visits/{instance.pk}/{uuid.uuid4()}-{filename}"


class SiteVisit(models.Model):
    name = NameField()
    slug = SlugField()
    cover_image = models.ImageField(
        upload_to=upload_site_visit_cover_image_to_func, verbose_name=_("Cover Image")
    )
    description = RichTextField()
    language = LanguageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entries = SiteVisitManager()

    class Meta:
        verbose_name = _("Site Visit")
        verbose_name_plural = _("Site Visits")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("apps.activities:site-visit-detail", kwargs={"slug": self.slug})

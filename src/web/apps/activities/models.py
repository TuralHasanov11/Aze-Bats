from __future__ import annotations

from io import BytesIO
import uuid
from typing import Optional
from django.utils.text import slugify
from apps.shared.models import (
    LanguageField,
    NameField,
    SlugField,
)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.shared.specification import Specification
from tinymce import models as tinymce_models
from django.dispatch import receiver
from PIL import Image
import os
from django.db.models.signals import pre_save
import logging


logger = logging.getLogger(__name__)

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
    if isinstance(instance, Project):
        return f"projects/{instance.slug}/{uuid.uuid4()}-{filename}"
    raise ValueError("Invalid instance type for upload_project_cover_image_to_func")


class Project(models.Model):
    name = NameField()
    slug = SlugField()
    cover_image = models.ImageField(
        upload_to=upload_project_cover_image_to_func, verbose_name=_("Cover Image")
    )
    description = tinymce_models.HTMLField(verbose_name=_("Description"))
    language = LanguageField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update Date"))

    entries = ProjectManager()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("apps.activities:project-detail", kwargs={"slug": self.slug})


@receiver(pre_save, sender=Project)
def convert_project_cover_image_to_webp(sender, instance: Project, **kwargs):
    if instance.cover_image:
        try:
            image = Image.open(instance.cover_image)
            webp_buffer = BytesIO()
            image.save(webp_buffer, 'WEBP')
            webp_buffer.seek(0)

            filename, _ = os.path.splitext(os.path.basename(instance.cover_image.name))
            new_filename = filename + '.webp'
            instance.cover_image.save(new_filename, webp_buffer, save=False)
        except Exception as e:
            logger.error("Error converting image to WebP for Project with id = %s: %s", instance.pk, e)
            raise e

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
    if isinstance(instance, SiteVisit):
        return f"site_visits/{instance.slug}/{uuid.uuid4()}-{filename}"
    raise ValueError("Invalid instance type for upload_site_visit_cover_image_to_func")


class SiteVisit(models.Model):
    name = NameField()
    slug = SlugField()
    cover_image = models.ImageField(
        upload_to=upload_site_visit_cover_image_to_func, verbose_name=_("Cover Image")
    )
    description = tinymce_models.HTMLField(verbose_name=_("Description"))
    language = LanguageField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update Date"))

    entries = SiteVisitManager()

    class Meta:
        verbose_name = _("Field Trip")
        verbose_name_plural = _("Field Trips")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("apps.activities:field-trip-detail", kwargs={"slug": self.slug})


@receiver(pre_save, sender=SiteVisit)
def convert_site_visit_image_to_webp(sender, instance: SiteVisit, **kwargs):
    if instance.cover_image:
        try:
            image = Image.open(instance.cover_image)
            webp_buffer = BytesIO()
            image.save(webp_buffer, 'WEBP')
            webp_buffer.seek(0)

            filename, _ = os.path.splitext(os.path.basename(instance.cover_image.name))
            new_filename = filename + '.webp'
            instance.cover_image.save(new_filename, webp_buffer, save=False)

        except Exception as e:
            logger.error("Error converting image to WebP for SiteVisit with id = %s: %s", instance.pk, e)
            raise e
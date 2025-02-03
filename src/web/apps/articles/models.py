from __future__ import annotations
from typing import Optional
from django.db import models

from apps.shared.models import NameField
from apps.shared.specification import Specification
from django.utils.translation import gettext_lazy as _


class ArticleManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()

    def get_by_id(self, id: int) -> Optional[Article]:
        return self.get_queryset().filter(id=id).first()

    def list(self, specification: Optional[Specification[Article]] = None) -> models.QuerySet[Article]:
        if specification:
            return specification.handle(self.get_queryset())
        return self.get_queryset().all()


class Article(models.Model):
    name = NameField()
    url = models.URLField(blank=False, null=False)
    author = models.CharField(null=False, blank=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entries = ArticleManager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.name

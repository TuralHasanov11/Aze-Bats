from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import Collection, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce import models as tinymce_models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
import os

from apps.shared.models import LanguageField
import logging


logger = logging.getLogger(__name__)

    
class CarouselItem(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    sub_title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Sub Title'))
    image = models.ImageField(upload_to='carousel/', verbose_name=_('Image'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        ordering = ['order']
        verbose_name = _('Carousel Item')
        verbose_name_plural = _('Carousel Items')

    def __str__(self):
        return self.title
    
    @property
    def image_extension(self):
        if self.image:
            return os.path.splitext(self.image.name)[1].lower()
        return ''
    
    
@receiver(pre_save, sender=CarouselItem)
def convert_carousel_item_image_to_webp(sender, instance: CarouselItem, **kwargs):
    if instance.image:
        try:
            image = Image.open(instance.image)
            webp_buffer = BytesIO()
            image.save(webp_buffer, 'WEBP')
            webp_buffer.seek(0)

            filename, _ = os.path.splitext(os.path.basename(instance.image.name))
            new_filename = filename + '.webp'
            instance.image.save(new_filename, webp_buffer, save=False)
        except Exception as e:
            logger.error("Error converting image to WebP for CarouselItem with id = %s: %s", instance.pk, e)
            raise e


class StaticTextKeys(models.TextChoices):
    ABOUT = "about", _("About")
    PRIVACY_POLICY = "privacy_policy", _("Privacy Policy")

class StaticTextManager(models.Manager):
    def single(self, key, language="en") -> Optional[StaticText]:
        return self.filter(key=key, language=language).first()


class StaticText(models.Model):
    key = models.CharField(max_length=50, choices=StaticTextKeys, verbose_name=_("Key"))
    language = LanguageField()
    content = tinymce_models.HTMLField(verbose_name=_("Content"))
    
    entries = StaticTextManager()
    
    class Meta:
        unique_together = ("key", "language")
        verbose_name = _("Static Text")
        verbose_name_plural = _("Static Texts")

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
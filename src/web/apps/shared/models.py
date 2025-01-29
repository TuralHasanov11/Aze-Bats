import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.template.defaultfilters import slugify


class RichTextField(models.TextField):
    description = _("Rich text editor field")

    def __init__(self, *args, **kwargs):
        kwargs["null"] = True
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class LanguageField(models.CharField):
    description = _("Language field")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2
        kwargs["choices"] = settings.LANGUAGES
        kwargs["default"] = settings.LANGUAGE_CODE
        super().__init__(*args, **kwargs)


class SlugField(models.SlugField):
    description = _("Slug field")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        kwargs["null"] = True
        kwargs["blank"] = True
        kwargs["unique"] = True
        super().__init__(*args, **kwargs)


class NameField(models.CharField):
    description = _("Name field")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        kwargs["null"] = False
        kwargs["blank"] = False
        super().__init__(*args, **kwargs)


class ImageField(models.ImageField):
    def __init__(
        self, directory: str, description: str = _("Image field"), *args, **kwargs
    ):
        def upload_to_func(instance: models.Model, filename: str) -> str:
            return f"{directory}/{slugify(str(instance))}/{uuid.uuid4()}-{filename}"

        self.upload_to = upload_to_func
        self.description = description

        super().__init__(*args, **kwargs)

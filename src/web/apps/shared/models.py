from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class LanguageField(models.CharField):
    description = _("Language")
    verbose_name = _("Language")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2
        kwargs["choices"] = settings.LANGUAGES
        kwargs["default"] = settings.LANGUAGE_CODE
        super().__init__(*args, **kwargs)


class SlugField(models.SlugField):
    description = _("Slug")
    verbose_name = _("Slug")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        kwargs["null"] = True
        kwargs["blank"] = True
        kwargs["unique"] = True
        super().__init__(*args, **kwargs)


class NameField(models.CharField):
    description = _("Name")
    verbose_name = _("Name")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        kwargs["null"] = False
        kwargs["blank"] = False
        super().__init__(*args, **kwargs)



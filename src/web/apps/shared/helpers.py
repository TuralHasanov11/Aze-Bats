import uuid
from django.db import models

from django.template.defaultfilters import slugify


def generate_slug(value: str) -> str:
    return slugify(value) + f"{uuid.uuid4()}"


class UploadImageStrategy:
    directory: str

    def __init__(self, directory: str) -> None:
        self.directory = directory

    def upload_to(self, instance: models.Model, filename: str) -> str:
        return f'{self.directory}/{slugify(str(instance))}/{uuid.uuid4()}-{filename}'

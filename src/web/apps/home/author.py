import json
from pathlib import Path
from django.conf import settings
from .models import Author, SocialLink
from django.templatetags.static import static

def load_author_data(language='en'):
    file_path = Path(settings.BASE_DIR) / 'apps/home/author.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    author_data = data.get(language, {})
    social_links_data = data.get('social_links', [])

    social_links = [SocialLink(name=link['name'], url=link['url'], icon=link['icon']) for link in social_links_data]

    return Author(
        name=author_data.get('name', ''),
        specialty=author_data.get('specialty', ''),
        profile_image=static(data.get('profile_image', '')),
        bio=author_data.get('bio', ''),
        social_links=social_links,
        email=data.get('email', '')
    )
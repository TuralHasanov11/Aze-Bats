from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.utils.translation import get_language

from apps.articles.models import Article

import logging

logger = logging.getLogger(__name__)

class ArticleListView(View):
    http_method_names = ["get"]
    paginate_by = 10

    def get(self, request: HttpRequest):
        page = int(request.GET.get("page", 1))
        articles = Paginator(
            Article.entries.list(get_language()), self.paginate_by
        ).get_page(page)
        return render(request, "articles/list.html", {"articles": articles})

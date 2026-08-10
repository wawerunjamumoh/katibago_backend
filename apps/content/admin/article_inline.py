from django.contrib import admin
from ..models.article import Article

class ArticleInline(admin.TabularInline):
    model = Article
    extra  = 1
    fields = (
        "article_number",
        "official_title",
        "citizen_title",
        "difficulty",
        "is_active",
    )
    show_change_link = True
    
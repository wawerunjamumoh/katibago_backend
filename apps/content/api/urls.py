from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views.article_view import ArticleViewSet


router = DefaultRouter()

router.register(
    "articles",
    ArticleViewSet,
    basename="article",
)


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
]

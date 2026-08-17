from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.chapter_view import ChapterViewSet
from .views.part_view import PartViewSet
from .views.article_view import ArticleViewSet
from .views.case_view import CaseViewSet
from .views.decision_view import DecisionPointViewSet
from .views.choice_view import ChoiceViewset
from .views.feedback_view import FeedbackViewSet
from .views.official_constitution_view import OfficialConstitutionViewSet
from .views.saftey_shield_view import SafteyShieldViewset



router = DefaultRouter()

# /api/chapters/
router.register(
    "chapters",
    ChapterViewSet,
    basename="chapter"
)

# /api/parts/
router.register(
    "parts",
    PartViewSet,
    basename="part"
)
# /api/articles/
router.register(
    "articles",
    ArticleViewSet,
    basename="article",
)
# /api/cases/
router.register(
    "cases",
    CaseViewSet,
    basename="case",
)

# /api/decisionpoints/
router.register(
    "decisionpoints",
    DecisionPointViewSet,
    basename="decisionpoint",
)

# /api/choices/
router.register(
    "choices",
    ChoiceViewset,
    basename="choice",
)

# /api/feedbacks/
router.register(
    "feedbacks",
    FeedbackViewSet,
    basename="feedback",
)

# /api/constitution/
router.register(
    "constitution",
    OfficialConstitutionViewSet,
    basename="constitution",
)

# /api/safteyshield/
router.register(
    "safteyshields",
    SafteyShieldViewset,
    basename="safteyshield"
)



urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
]

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
from .views.article_progress_view import MyProgressDetailView, MyProgressListView



router = DefaultRouter()

# /api/chapters/
router.register(
    "chapters",
    ChapterViewSet,
    basename="chapter"
)

# /api/v1/parts/
router.register(
    "parts",
    PartViewSet,
    basename="part"
)
# /api/v1/articles/
router.register(
    "articles",
    ArticleViewSet,
    basename="article",
)
# /api/v1/cases/
router.register(
    "cases",
    CaseViewSet,
    basename="case",
)

# /api/v1/decisionpoints/
router.register(
    "decisionpoints",
    DecisionPointViewSet,
    basename="decisionpoint",
)

# /api/v1/choices/
router.register(
    "choices",
    ChoiceViewset,
    basename="choice",
)

# /api/v1/feedbacks/
router.register(
    "feedbacks",
    FeedbackViewSet,
    basename="feedback",
)

# /api/v1/constitution/
router.register(
    "constitution",
    OfficialConstitutionViewSet,
    basename="constitution",
)

# /api/v1/safteyshield/
router.register(
    "safteyshields",
    SafteyShieldViewset,
    basename="safteyshield"
)



urlpatterns = [
    path("auth/", include("apps.content.api.v1.auth_urls")),
    path("me/progress/", MyProgressListView.as_view(), name="my-progress-list"),
    path(
        "me/progress/<int:article_number>/",
        MyProgressDetailView.as_view(),
        name="my-progress-detail",
    ),
    path("", include(router.urls)),
]

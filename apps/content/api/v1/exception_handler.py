from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from apps.content.exceptions import ArticleNotFoundError


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return response

    if isinstance(exc, ArticleNotFoundError):
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, ValueError):
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return None

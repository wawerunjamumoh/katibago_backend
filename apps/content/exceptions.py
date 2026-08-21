class ArticleNotFoundError(Exception):
    """Raised when article cannot be found"""

class ArticleNotReadyError(Exception):
    """Raised when an article does not satisfy publication requirements."""

class ArticleNotPublishedError(Exception):
    """Raised when an unpublished article is activated."""

class ArticleNotStartedError(Exception):
    """Raised when an article complete request comes throug before a lesson is started"""
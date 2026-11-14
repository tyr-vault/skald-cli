"""Application exceptions."""


class SkaldError(Exception):
    """Base error for Skald."""


class NotInitializedError(SkaldError):
    """Workspace or database not initialized."""


class ConfigurationError(SkaldError):
    """Invalid or missing configuration."""


class RepositoryError(SkaldError):
    """Repository validation or scan failure."""


class NotFoundError(SkaldError):
    """Entity not found in knowledge base."""

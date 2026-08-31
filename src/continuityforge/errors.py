class ContinuityForgeError(Exception):
    """Base exception for expected project errors."""


class ValidationError(ContinuityForgeError):
    """Raised when an episode or configuration is invalid."""


class PlanningError(ContinuityForgeError):
    """Raised when a story beat cannot fit the supported shot windows."""


class RoutingError(ContinuityForgeError):
    """Raised when no configured model can handle a shot."""


class GenerationError(ContinuityForgeError):
    """Raised when a provider call cannot be completed safely."""


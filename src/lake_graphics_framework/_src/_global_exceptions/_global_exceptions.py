"""
Globally accessable exceptions throughout the lake graphics framework.
"""


class GraphicsInitError(RuntimeError):
    """Raised when the graphics subsystem fails to initialize."""


class WindowInitError(RuntimeError):
    """Raised when the window fails to initialize."""


CustomErrors = GraphicsInitError | WindowInitError

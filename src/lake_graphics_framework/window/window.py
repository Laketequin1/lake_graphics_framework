"""
Creates an application window with a rendering loop.

Handles GLFW initialization, window creation, input setup,
event processing, and delegates rendering tasks to a GraphicsEngine.
"""


from .._src._global_type_hinting import Size, PositiveInt
#from .._src.


class Window:
    """
    Creates an application window with a rendering loop.

    Handles GLFW initialization, window creation, input setup,
    event processing, and delegates rendering tasks to a GraphicsEngine.
    """
    def __init__(self,
        size: Size = (1280, 720),
        caption: str = "GLFW Window :)",
        *,
        fullscreen: bool = False,
        resizable: bool = False,
        borderless: bool = False,
        max_fps: None | PositiveInt = None,
        vsync: bool = True
    ) -> None:
        """
        TODO

        Args:
            size (Size): Window width & height.
                Defaults to (1280, 720).
            caption (str): Window title.
                Defaults to "GLFW Window".
            fullscreen (bool): Whether the window should be fullscreen.
                Defaults to False.
            resizable (bool): Whether the window can be resized.
                Defaults to True.
            borderless (bool): Whether the window has a border.
                Defaults to False.
            max_fps (None | PositiveInt): Uncapped fps if None,
                otherwise frames per second can't exceed max_fps.
                Defaults to None.
            vsync (bool): Whether to enable vsync.
                Defaults to True.
        """
        pass

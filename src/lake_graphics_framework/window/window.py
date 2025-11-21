"""
Creates an application window with a rendering loop.

Handles GLFW initialization, window creation, input setup,
event processing, and delegates rendering tasks to a GraphicsEngine.
"""


from uuid import uuid4 as uuid
from threading import Lock, Event


import glfw # type: ignore
import OpenGL.GL as gl # type: ignore


from .._src._global_type_hinting import Size, PositiveInt, Optional
from .._src._global_exceptions import GraphicsInitError, WindowInitError
from .._variable_validation import validate_type, validate_types
from .._message_logger import log


SWAP_INTERVAL_UNLOCKED = 0
SWAP_INTERVAL_VSYNC = 1


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
        max_fps: Optional[PositiveInt] = None,
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
            max_fps (Optional[PositiveInt]): Uncapped fps if None,
                otherwise frames per second can't exceed max_fps.
                Defaults to None.
            vsync (bool): Whether to enable vsync. Overrides max_fps.
                Defaults to True.
        """
        self.uuid = uuid()
        log.info(f"Creating window {self.uuid}.")

        validate_types(
            [
                ('size', size, Size),
                ('caption', caption, str),
                ('fullscreen', fullscreen, bool),
                ('resizable', resizable, bool),
                ('borderless', borderless, bool),
                ('max_fps', max_fps, Optional[PositiveInt]),
                ('vsync', vsync, bool)
            ]
        )

        self.size = size
        self.caption = caption
        self.fullscreen = fullscreen
        self.resizable = resizable
        self.borderless = borderless
        self.max_fps = max_fps
        self.vsync = vsync

        log.info(
            f"Window {self.uuid}: Variable validation passed. "
            f"Variables: {self.__dict__}"
        )

        # Set variables
        self.requesting_close = False
        self.should_close_event = Event()
        self.lock = Lock()

        self.monitor, self.video_mode = self._init_display()
        log.dev("TODO: Allow monitor selection for window.")

        self.display_size = self.video_mode.size
        log.info(f"Window {self.uuid}: Display size {self.display_size}")

        self._enforce_fullscreen_constraints()

        if self.size[1] != 0:
            self.aspect_ratio = self.size[0] / self.size[1]
            log.info(
                f"Window {self.uuid}: Aspect ratio of {self.aspect_ratio}."
            )
        else:
            log.warn(
                f"Window {self.uuid}: height of 0... rightttt. "
                "Assuming an aspect ratio of 1."
            )
            self.aspect_ratio = 1

        self.window = self._init_window(
            self.monitor,
            self.size,
            self.caption,
            self.fullscreen,
            self.vsync
        )

        log.info(
            f"Window creation passed for {self.uuid}. "
            f"New Variables: {self.__dict__}"
        )

    def _enforce_fullscreen_constraints(self):
        """
        [Private]
        Ensures window flags are valid for fullscreen windows.
        'Fullscreen' takes priority over 'resizable' and 'borderless'.
        """
        log.dev("TODO: Verify resizable & borderless functionality.")

        if not self.fullscreen:
            return

        if self.resizable:
            self.resizable = False
            log.warn(
                f"Window {self.uuid}: 'resizable' disabled "
                "due to fullscreen mode."
            )

        if self.borderless:
            self.borderless = False
            log.warn(
                f"Window {self.uuid}: 'borderless' ignored "
                "due to fullscreen mode."
            )

        self.size = self.display_size
        log.info(
            f"Window {self.uuid}: Fullscreen, "
            f"updated size from {self.size} to {self.display_size}."
        )

    @staticmethod
    def _init_display() -> tuple[glfw._GLFWmonitor, glfw._GLFWvidmode]: # type: ignore
        """
        [Private]
        Initializes the GLFW display by setting up the primary monitor
        and video mode.
        
        It ensures that GLFW can be initialized, the primary monitor can
        be found, and a valid video mode is available. An exception is
        raised if anything fails.
        
        Returns:
            tuple[glfw._GLFWmonitor, glfw._GLFWvidmode]: The primary
                monitor and its video mode.

        Raises:
            GraphicsInitError: If window initiation fails.
        """
        if not glfw.init():
            log.error("GLFW can't be initialized.", GraphicsInitError)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3) # type: ignore
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3) # type: ignore
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE) # type: ignore
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE) # type: ignore

        monitor = glfw.get_primary_monitor()
        if not monitor:
            log.error("GLFW can't find the primary monitor", GraphicsInitError)

        video_mode = glfw.get_video_mode(monitor) # type: ignore
        if not video_mode:
            log.error("GLFW can't get video mode", GraphicsInitError)

        return monitor, video_mode

    def _init_window(
            self,
            monitor: glfw._GLFWmonitor, # type: ignore
            size: Size,
            caption: str,
            fullscreen: bool,
            vsync: bool
        ) -> glfw._GLFWwindow: # type: ignore
        """
        [Private]
        Initializes the GLFW window and associates it with the primary
        monitor. Sets the frame rate limit based on the 'vsync' and
        'max_fps' parameters. If the window creation fails, GLFW is
        terminated and an exception is raised.
        
        Parameters:
            monitor (glfw._GLFWmonitor): The primary monitor to use
                for fullscreen.
            size (Size): The desired size of the window (width, height).
            caption (str): The title of the window.
            fullscreen (bool): If the window should be fullscreen.
            vsync (bool): Whether vsync should be enabled.
                Overrides max_fps.

        Raises:
            ...

        Returns:
            glfw._GLFWwindow: The created window.
        """
        screen_monitor = monitor if fullscreen else None

        window = glfw.create_window( # type: ignore
            *size,
            caption,
            screen_monitor,
            None
        )
        if not window:
            glfw.terminate()
            log.error("GLFW window can't be created", WindowInitError)

        glfw.make_context_current(window) # type: ignore
        if not fullscreen:
            self._center_window(window, monitor, size)

        # Set vsync if enabled
        swap_interval = (
            SWAP_INTERVAL_VSYNC
            if vsync
            else SWAP_INTERVAL_UNLOCKED
        )
        self.set_swap_interval(swap_interval) # type: ignore

        return window

    def _center_window(
            self,
            window: glfw._GLFWwindow, # type: ignore
            monitor: glfw._GLFWmonitor, # type: ignore
            size: Size
        ) -> None:
        """
        [Private]
        Centers the GLFW window within the working area of the
        specified monitor.

        Parameters:
            window (glfw._GLFWwindow): The GLFW window to be centered.
            monitor (glfw._GLFWmonitor): The monitor whose work area is
                used for positioning.
            size (Size): The dimensions of the window (width, height).
        """
        log.info(f"Centering window {self.uuid}.")

        x, y, width, height = glfw.get_monitor_workarea(monitor) # type: ignore

        pos_x = x + (width - size[0]) // 2
        pos_y = y + (height - size[1]) // 2

        glfw.set_window_pos(window, pos_x, pos_y) # type: ignore

    def set_swap_interval(self, swap_interval: int) -> None:
        """
        Sets the swap interval (vsync) for the current glfw window.

        This is also called vsync / vertical synchronization.

        The swap interval is the number of screen updates to wait from
        the time swap buffers was called to swapping the buffers.

        Accepts negative swap intervals, which allows the driver to swap
        immediately even if a frame arrives a little bit late.

        Note:
            A swap interval of 1 represents vsync on.
            A swap interval of 0 represents vsync off (unlocked).

        Args:
            swap_interval (int): The minimum number of screen updates to
                wait for until the buffers are swapped.
        """
        validate_type("swap_interval", swap_interval, int)

        log.info(
            f"Window {self.uuid}: "
            f"Updating glfw swap interval to {swap_interval}."
            )
        glfw.swap_interval(swap_interval) # type: ignore

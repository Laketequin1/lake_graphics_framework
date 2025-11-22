"""
Creates a window event handler for the Window.

Includes mouse movement, key presses, and window events.
"""


from dataclasses import dataclass
from threading import Event


import glfw # type: ignore


from .._variable_validation import validate_type
from .window import Window
from .._message_logger import log


@dataclass
class KeyState:
    """
    Represents the state of a keyboard key.
    
    Includes whether it is held down, when it was pressed or released,
    and how long it has been held.
    """
    is_down: bool = False
    just_pressed: bool = False
    just_released: bool = False


class EventHandler:
    """
    [Private]

    Event handling for the window.
    """
    def __init__(self, window: Window) -> None:
        log.info(f"Creating event handler for {window.uuid}.")

        validate_type("window", window, Window)
        self._window = window

        self._key_states: dict[int, KeyState] = {}
        self._window_requesting_close = False
        self._should_close_event = Event()

        log.info(f"Created event handler for {window.uuid}.")

    def init_key_input(self) -> None:
        """
        Initiate key callback for the current window.
        """
        log.info(f"Setting up key callback for {self.window.uuid}.")
        glfw.set_key_callback(self._window, self._key_callback) # type: ignore

    def _key_callback(
        self,
        _window: glfw._GLFWwindow, # type: ignore
        key: int,
        _scancode: int,
        action: int,
        _mods: int
    ) -> None:
        """
        [Private]
        Key callback to updates the local saved key states.
        """
        if key == glfw.KEY_UNKNOWN:
            return

        if key not in self._key_states:
            self._key_states[key] = KeyState()

        current_key = self._key_states[key]

        if action == glfw.PRESS:
            current_key.is_down = True
            current_key.just_pressed = True
        elif action == glfw.RELEASE:
            current_key.is_down = False
            current_key.just_released = True

    def _handle_window_events(self) -> None:
        """
        [Private]
        Handle GLFW events to check if the window should close.
        """
        if glfw.window_should_close(self._window): # type: ignore
            self._window_requesting_close = True
            log.info(f"Window {self._window.uuid} event requesting close")

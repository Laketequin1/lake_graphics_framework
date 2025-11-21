"""
Example usage of the variable validaiton.
"""


try:
    from src.lake_graphics_framework._variable_validation import (
        validate_types,
        validate_type
    )
    from src.lake_graphics_framework._src._global_type_hinting import Size
except ImportError:
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.lake_graphics_framework._variable_validation import (
        validate_types,
        validate_type
    )
    from src.lake_graphics_framework._src._global_type_hinting import Size


def main():
    """
    Test!
    """
    size = (0, 0)
    caption = "Title"
    max_fps = 100
    print_gl_errors = True
    validate_types(
        [
            ('size', size, Size),
            ('caption', caption, str),
            ('max_fps', max_fps, int),
            ('print_gl_errors', print_gl_errors, bool)
        ]
    ) # OK

    print("OK 1")

    vsync = False
    validate_type('vsync', vsync, bool) # OK

    print("OK 2")

    size = (0, -20) # Set to an invalid size
    validate_types(
        [
            ('size', size, Size), # This part contains an invalid size
            ('caption', caption, str),
            ('max_fps', max_fps, int),
            ('print_gl_errors', print_gl_errors, bool)
        ]
    ) # Fails type check, raises error

    print("NOT OK :< ")


if __name__ == "__main__":
    main()

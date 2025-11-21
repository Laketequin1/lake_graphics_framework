"""
Example usage for the logger feature.
"""


try:
    from src.lake_graphics_framework._message_logger import log
except ImportError:
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.lake_graphics_framework._message_logger import log


def main():
    """
    Test!
    """
    # Initialize the logger with a specific verbosity level
    verbose_level = "DEV"  # "NONE", "LOG_ONLY", "ERROR", "WARNING", "CRUCIAL", "INFO", or "DEV"
    log_folder = "logs/"

    # Initialize the log with the specified verbose level
    log.init(verbose_level, log_folder)

    # Log different types of messages to demonstrate functionality
    log.error("This is an error message.")
    log.warn("This is a warning message.")
    log.crucial("This is a crucial message.")
    log.info("This is an info message.")
    log.dev("This is an developer note.")

    # If you want to test other verbose levels, you can change the level and log more messages
    log.set_verbose_type("WARNING")
    log.info("This info message should not be printed, but will appear in the log file.")
    log.warn("This warning message should still be printed.")
    log.error("This error message should still be printed.")

    # Nothing gets logged, nothing written to file.
    log.set_verbose_type("NONE")
    log.error("This error won't print and won't write to the log file :)")


if __name__ == "__main__":
    main()

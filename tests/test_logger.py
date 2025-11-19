"""
Example usage for the logger feature.
"""


try:
    from src.lake_graphics_framework.message_logger import MessageLogger
except ImportError:
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.lake_graphics_framework.message_logger import MessageLogger


def main():
    """
    Test!
    """
    # Initialize the logger with a specific verbosity level
    verbose_level = "DEV"  # "NONE", "LOG_ONLY", "ERROR", "WARNING", "CRUCIAL", "INFO", or "DEV"
    log_folder = "logs/"

    # Initialize the MessageLogger with the specified verbose level
    MessageLogger.init(verbose_level, log_folder)

    # Log different types of messages to demonstrate functionality
    MessageLogger.error("This is an error message.")
    MessageLogger.warn("This is a warning message.")
    MessageLogger.crucial("This is a crucial message.")
    MessageLogger.info("This is an info message.")
    MessageLogger.dev("This is an developer note.")

    # If you want to test other verbose levels, you can change the level and log more messages
    MessageLogger.set_verbose_type("WARNING")
    MessageLogger.info("This info message should not be printed, but will appear in the log file.")
    MessageLogger.warn("This warning message should still be printed.")
    MessageLogger.error("This error message should still be printed.")

    # Nothing gets logged, nothing written to file.
    MessageLogger.set_verbose_type("NONE")
    MessageLogger.error("This error won't print and won't write to the log file :)")


if __name__ == "__main__":
    main()

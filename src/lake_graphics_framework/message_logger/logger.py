"""
Used for debugging during production and deployment by logging to the
console and saving to a designated log file.

Logs messages to a timestamped log file under the "logs/" folder.
"""


import os

from datetime import datetime
from typing import Literal, NoReturn



class MessageLogger:
    """
    Used for debugging purposes during production. When initialized, set
    a verbose level of increasingly more information.

    Logs messages to a timestamped log file under the "logs/" folder.

    Supported levels include:
    - NONE:     Completely ignores all logs.
    - LOG_ONLY: Saves all logs to a file without printing.
    - ERROR:    Prints only error messages.                 (logs all)
    - WARNING:  Prints warnings and errors.                 (logs all)
    - CRUCIAL:  Prints warnings, errors, and crucial.       (logs all)
    - INFO:     Prints all message levels.                  (logs all)
    - DEV:      Prints all message levels and dev notes.    (logs all)    
    """
    _LOG_FOLDER = "logs/"
    _LOG_FILENAME = datetime.now().strftime("%Y-%m-%d_%H.%M.%S") + ".log"
    _LOG_FILEPATH = _LOG_FOLDER + _LOG_FILENAME

    _ERROR_IF_NOT_INITIATED = True

    _VERBOSITY_PRIORITYS = {
        "NONE":     0,  # Everything completely ignored
        "LOG_ONLY": 1,  # Only log to file
        "ERROR":    2,  # Only print errors
        "WARNING":  3,  # Only print warnings and errors
        "CRUCIAL":  4,  # Only print warnings, errors, and crucial info
        "INFO":     5,  # Print all
        "DEV":      6   # Print all and developer notes
    }

    _VERBOSITY_KEYS = tuple(_VERBOSITY_PRIORITYS.keys())
    _VerbosityLiteral = Literal[
        "NONE",
        "LOG_ONLY",
        "ERROR",
        "WARNING",
        "CRUCIAL",
        "INFO",
        "DEV"
    ]

    _TEXT_STYLES = {
        "ERROR":   "\033[31m",  # Red
        "WARNING": "\033[33m",  # Yellow
        "CRUCIAL": "\033[97m",  # White
        "INFO":    "\033[90m",  # Light Grey
        "DEV":     "\033[32m",  # Green
        "CLEAR":   "\033[0m"    # Reset
    }

    _SETUP_MESSAGE_FORMAT = (
        "Logfile created with "
        "verbose level {verbosity_priority} "
        "on {date_time}. "
        "Have fun <3\n"
    )
    _PREFIX_SPACE_PADDING = 7

    # Verbose unset
    _verbosity_priority = -1
    _logs: list[str] = []

    @classmethod
    def init(cls, verbosity: _VerbosityLiteral) -> None:
        """
        Initializes a MessageLogger instance with a specified verbose level.
        Will throw a ValueError if verbose level is invalid.

        Parameters:
            verbosity (str): The verbosity level for logging.
                - NONE:     Completely ignores all logs.
                - LOG_ONLY: Saves all logs to a file without printing.
                - ERROR:    Prints only error messages.                (logs all)
                - WARNING:  Prints warnings and errors.                (logs all)
                - CRUCIAL:  Prints warnings, errors, and crucial.      (logs all)
                - INFO:     Prints all message levels.                 (logs all)
                - DEV:      Prints all message levels and dev notes.   (logs all)
        """
        cls.set_verbose_type(verbosity)
        cls._logs = []

        date_time = datetime.now().strftime("%d/%m/%Y at %H:%M:%S")

        setup_message = cls._SETUP_MESSAGE_FORMAT.format(
            verbosity_priority=cls._VERBOSITY_KEYS[cls._verbosity_priority],
            date_time=date_time
        )

        cls._setup_log_file(setup_message)

    @classmethod
    def _setup_log_file(cls, setup_message: str) -> None:
        """
        [Private]
        Generates the log folder if it doesn't exist. Creates a new log
        file and writes the initial setup message.

        Parameters:
            setup_message (str): The message to write at the beginning
                                 of the log file.
        """
        os.makedirs(cls._LOG_FOLDER, exist_ok=True)

        with open(cls._LOG_FILEPATH, "w", encoding="utf-8") as log_file:
            log_file.write(setup_message + "\n")

    @classmethod
    def check_init_completed(cls) -> bool:
        """
        Returns if the class has been initiated.

        Returns:
            bool: If ClassLogger initiation has been completed.
        """
        if cls._verbosity_priority == -1:
            return False
        return True

    @classmethod
    def error(
            cls, message: str, exception: Exception | None = None
        ) -> None:
        """
        Logs an error message to the file and prints to the terminal
        based on the verbose level.
        
        If provided with an exception, will raise the exception after
        log processing.

        Parameters:
            message (str): The error message to be logged.
            exception (Exception | None): Optional exception to raise.
        """
        cls._log("ERROR", str(message))

        if exception is not None:
            raise exception

    @classmethod
    def warn(cls, message: str) -> None:
        """
        Logs a warning message to the file and prints to the terminal
        based on the verbose level.

        Parameters:
            message (str): The warning message to be logged.
        """
        cls._log("WARNING", str(message))

    @classmethod
    def crucial(cls, message: str) -> None:
        """
        Logs a crucial message to the file and prints to the terminal
        based on the verbose level.

        Parameters:
            message (str): The warning message to be logged.
        """
        cls._log("CRUCIAL", str(message))

    @classmethod
    def info(cls, message: str) -> None:
        """
        Logs a info message to the file and prints to the terminal based
        on the verbose level.

        Parameters:
            message (str): The warning message to be logged.
        """
        cls._log("INFO", str(message))

    @classmethod
    def dev(cls, message: str) -> None:
        """
        Logs a developer note message to the file and prints to the
        terminal based on the verbose level.

        Parameters:
            message (str): The developer note message to be logged.
        """
        cls._log("DEV", str(message))

    @classmethod
    def set_verbose_type(cls, verbosity: _VerbosityLiteral) -> None:
        """
        Updates the verbose level.
        Will throw a ValueError if verbose level is invalid.

        Parameters:
            verbosity (str): The verbosity level for logging.
                - NONE:     Completely ignores all logs.
                - LOG_ONLY: Saves all logs to a file without printing.
                - ERROR:    Prints only error messages.                (logs all)
                - WARNING:  Prints warnings and errors.                (logs all)
                - CRUCIAL:  Prints warnings, errors, and crucial.      (logs all)
                - INFO:     Prints all message levels.                 (logs all)
                - DEV:      Prints all message levels and dev notes.   (logs all)
        """
        cls._verbosity = str(verbosity
                            ).replace("\n", ""
                                ).replace("\r", ""
                                    ).strip().upper()

        if cls._verbosity not in cls._VERBOSITY_PRIORITYS:
            raise ValueError(
                f"Verbose level '{cls._verbosity}' is not an option. "
                f"Available options are: "
                f"{', '.join(cls._VERBOSITY_PRIORITYS.keys())}."
                )

        prev_verbosity_priority = cls._verbosity_priority
        cls._verbosity_priority = cls._VERBOSITY_PRIORITYS[cls._verbosity]

        if prev_verbosity_priority != -1:  # Check this isn't the init set
            prev_verbose_type = cls._VERBOSITY_KEYS[prev_verbosity_priority]
            cls.info(
                f"MessageLogger verbose type "
                f"updated from {prev_verbose_type} to {cls._verbosity}"
                )

    @classmethod
    def _log(cls, verbose_type: str, message: str) -> None:
        """
        [Private]
        Checks if init is completed, then handles the logging of
        messages, including formatting, saving to the file, and printing
        to the terminal dependant on verbose settings.

        Parameters:
            verbose_type (str): The type of message being logged.
                (e.g. "ERROR", "WARNING", "INFO", ...)
            message (str): The content of the message to be logged.
        """
        if not cls._check_init_completed():
            return

        if cls._verbosity_priority < cls._VERBOSITY_PRIORITYS["LOG_ONLY"]:
            return

        # Log message to file
        formatted_message = cls._format_message(verbose_type, message)
        cls._logs.append(message)
        cls._append_to_log_file(formatted_message)

        if cls._verbosity_priority < cls._VERBOSITY_PRIORITYS[verbose_type]:
            return

        # Print message to terminal
        styled_message = cls._style_message(verbose_type, formatted_message)
        print(styled_message)

    @classmethod
    def _style_message(cls, style: str, message: str) -> str:
        """
        [Private]
        Applies ANSI styling to a message for formatted terminal output.

        Parameters:
            style (str): The style to be applied from _TEXT_STYLES.
                (e.g. "ERROR", "WARNING", "INFO", ...)
            message (str): The message to be styled.

        Returns:
            str: The styled message.
        """
        styled_message = (
            cls._TEXT_STYLES[style] +
            str(message) +
            cls._TEXT_STYLES["CLEAR"]
        )
        return styled_message

    @classmethod
    def _format_message(cls, prefix: str, message: str) -> str:
        """
        [Private]
        Adds a timestamp and prefix to the beginning of the message.

        Parameters:
            prefix (str): The message prefix - indicating its type.
                (e.g., "ERROR", "INFO")
            message (str): The message to be formatted.

        Returns:
            str: The formatted message with a timestamp and prefix.
        """
        time = datetime.now().strftime("%H:%M:%S")
        padded_prefix = prefix.ljust(cls._PREFIX_SPACE_PADDING)

        new_line_occurances = message.count("\n")
        new_line_padding = "\n" + " "*(1+8+2+cls._PREFIX_SPACE_PADDING) + " : "
        padded_message = str(message).replace(
                            "\n",
                            new_line_padding,
                            new_line_occurances
                        )

        formatted_message = f"[{time}] {padded_prefix} : {str(padded_message)}"
        return formatted_message

    @classmethod
    def _append_to_log_file(cls, message: str) -> None:
        """
        [Private]
        Appends a formatted message to the log file.

        Parameters:
            message (str): The message to be written to the log file.
        """
        with open(cls._LOG_FILEPATH, "a", encoding="utf-8") as log_file:
            log_file.write(str(message) + "\n")

    @classmethod
    def _check_init_completed(cls) -> bool | NoReturn:
        """
        [Private]
        Check if ClassLogger has been initiated.
        Raises error if enabled and not initiated, otherwise returns the
        init status.

        Returns:
            bool | NoReturn: True if not initiated, False otherwise.
        """
        if cls._ERROR_IF_NOT_INITIATED and not cls.check_init_completed():
            raise RuntimeError(
                "MessageLogger has not been initialized. "
                "Make sure to call MessageLogger.init(verbosity)"
            )

        return cls.check_init_completed()

"""
Used for debugging during production and deployment by logging to the
console and saving to a designated log file.

Logs messages to a timestamped log file under the "logs/" folder.
"""

from .logger import MessageLogger

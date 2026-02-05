"""
Logging Module

Provides centralized logging configuration for the entire backend.
Supports both file-based logging and console output with configurable levels.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_ENABLED, LOG_LEVEL, LOG_DIR, LOG_FILE

# Log format: timestamp [level] module_name: message
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def setup_logging():
    """
    Initialize logging configuration.
    
    Sets up:
    - Root logger with configured level (DEBUG, INFO, WARNING, ERROR)
    - Rotating file handler to prevent log files from growing too large
    - Automatic log rotation when max bytes exceeded
    - UTF-8 encoding for international characters
    
    Configuration from config.py:
    - LOG_ENABLED: Enable/disable file logging
    - LOG_LEVEL: Logging level
    - LOG_DIR: Directory for log files
    - LOG_FILE: Log filename
    """
    root_logger = logging.getLogger()

    # Clear existing handlers
    root_logger.handlers.clear()

    # If logging disabled, use NullHandler to suppress all output
    if not LOG_ENABLED:
        root_logger.addHandler(logging.NullHandler())
        return

    # Create log directory if needed
    os.makedirs(LOG_DIR, exist_ok=True)

    # Set logging level from config
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(level)

    # Create formatter for all handlers
    formatter = logging.Formatter(LOG_FORMAT)

    # Create rotating file handler (max 2MB per file, keep 5 backup files)
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE),
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Add file handler to root logger
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Returns a named logger for use in specific modules. Loggers are typically
    named after the module name using __name__.
    
    Args:
        name (str): Logger name, usually __name__
        
    Returns:
        logging.Logger: Logger instance for the module
    Liefert einen benannten Logger zurück
    """
    return logging.getLogger(name)

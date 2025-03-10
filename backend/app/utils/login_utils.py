# backend/app/utils/logging_utils.py

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

# Log directory and file settings
LOG_DIR = "logs"
LOG_FILE = "app.log"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5  # Keep up to 5 backup log files

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name: str, log_level: int = logging.INFO, log_to_console: bool = True) -> logging.Logger:
    """
    Set up and configure a logger.

    Args:
        name (str): Name of the logger (usually __name__).
        log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG). Defaults to logging.INFO.
        log_to_console (bool): Whether to log to the console. Defaults to True.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create a file handler
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE),
        maxBytes=LOG_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a console handler (if enabled)
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

def log_message(logger: logging.Logger, level: int, message: str, extra: Optional[Dict[str, Any]] = None):
    """
    Log a message with the specified level and optional extra data.

    Args:
        logger (logging.Logger): Logger instance.
        level (int): Logging level (e.g., logging.INFO, logging.ERROR).
        message (str): Message to log.
        extra (Optional[Dict[str, Any]]): Additional data to include in the log. Defaults to None.
    """
    logger.log(level, message, extra=extra)

def log_error(logger: logging.Logger, message: str, exc_info: Optional[bool] = False, extra: Optional[Dict[str, Any]] = None):
    """
    Log an error message with optional exception information.

    Args:
        logger (logging.Logger): Logger instance.
        message (str): Error message to log.
        exc_info (Optional[bool]): Whether to include exception information. Defaults to False.
        extra (Optional[Dict[str, Any]]): Additional data to include in the log. Defaults to None.
    """
    logger.error(message, exc_info=exc_info, extra=extra)

def log_info(logger: logging.Logger, message: str, extra: Optional[Dict[str, Any]] = None):
    """
    Log an informational message.

    Args:
        logger (logging.Logger): Logger instance.
        message (str): Informational message to log.
        extra (Optional[Dict[str, Any]]): Additional data to include in the log. Defaults to None.
    """
    logger.info(message, extra=extra)

def log_debug(logger: logging.Logger, message: str, extra: Optional[Dict[str, Any]] = None):
    """
    Log a debug message.

    Args:
        logger (logging.Logger): Logger instance.
        message (str): Debug message to log.
        extra (Optional[Dict[str, Any]]): Additional data to include in the log. Defaults to None.
    """
    logger.debug(message, extra=extra)
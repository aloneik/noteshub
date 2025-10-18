"""Logging configuration for NoteHub Desktop."""

import logging
import sys
from pathlib import Path
from datetime import datetime

from config import DEBUG, LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT, LOGS_DIR


def setup_logging():
    """
    Setup application logging.
    
    In DEBUG mode:
        - Logs to both console and file
        - Level: DEBUG
        - Detailed format with timestamps
    
    In production mode:
        - Logs only to file
        - Level: INFO
        - Standard format
    """
    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Generate log filename with timestamp
    log_filename = LOGS_DIR / f"notehub_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    
    # Remove any existing handlers
    root_logger.handlers.clear()
    
    # File handler (always enabled)
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(LOG_LEVEL)
    file_formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler (only in DEBUG mode)
    if DEBUG:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            "%(levelname)s [%(name)s] %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
        logging.info("=" * 80)
        logging.info("DEBUG MODE ENABLED")
        logging.info(f"Log file: {log_filename}")
        logging.info("=" * 80)
    else:
        logging.info(f"NoteHub Desktop started - Log file: {log_filename}")
    
    return log_filename


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

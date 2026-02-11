"""
Logging utilities
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get or create a logger with consistent formatting
    
    Args:
        name: Logger name (usually __name__)
        level: Optional logging level (default: INFO)
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Only configure if not already configured
        if level is None:
            level = logging.INFO
        
        logger.setLevel(level)
        
        # Console handler with formatting
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger


def setup_root_logger(level: int = logging.INFO):
    """
    Setup root logger for application
    
    Args:
        level: Logging level
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )

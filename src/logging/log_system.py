# /////////////////////////////////////////////////////////////////////////////
# LOGGING SYSTEM 
#
# This module provides a logging system with configurable loggers. It allows the 
# creation of multiple loggers with different settings within a LoggerFactory class
#
# This module can be re-used across multiple applications. The actual loggers created 
# for use in an application are set up in a separate module (log_instances.py).
#
# Compulsory configurations:
#   1. logger name
#   2. log file path
#
# Optional configurations:
#   1. log level (default is INFO)
#   2. format of the log message (default is 'long' but console is always 'short')
#   3. whether to output to console as well (default is disabled)
#
# /////////////////////////////////////////////////////////////////////////////

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Dict, Any
from dataclasses import dataclass


# /////////////////////////////////////////////////////////////////////////////
@dataclass
class LogConfig:
    """Configuration settings for loggers"""
    FORMATS = {
        'long': {
            'msg': '%(asctime)s - %(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s',
            'date': '%d-%m-%Y %H:%M:%S'
        },
        'short': {
            'msg': '%(asctime)s - %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            'date': '%H:%M:%S'
        }
    }
    LOG_DIR: str = 'logs'
    MAX_BYTES: int = 1024 * 1024  # 1MB
    BACKUP_COUNT: int = 5



# /////////////////////////////////////////////////////////////////////////////
def setup_logger(
    logger_name: str,
    log_file: str,
    level: int = logging.INFO,
    format: str = 'long',
    console: bool = False
) -> logging.Logger:
    """Set up a logger with improved error handling"""
    
    try:
        ensure_log_directory_exists(log_file)
        logger = get_logger(logger_name)
        logger.setLevel(level)
        
        # Add rotating file handler
        file_handler = create_rotating_handler(log_file, format)
        logger.addHandler(file_handler)
        
        if console:
            console_handler = create_console_handler(format='short')
            logger.addHandler(console_handler)
            
        return logger
    except Exception as e:
        raise RuntimeError(f"Failed to setup logger {logger_name}: {e}")


# /////////////////////////////////////////////////////////////////////////////
def ensure_log_directory_exists(log_path: str) -> None:
    """Ensure log directory exists"""
    
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create log directory: {e}")
    
      
# /////////////////////////////////////////////////////////////////////////////
def get_logger(logger_name):
  """Get a logger by name."""
  
  logger = logging.getLogger(logger_name)
  if logger.hasHandlers():
    logger.handlers.clear()
  
  return logger


# /////////////////////////////////////////////////////////////////////////////
def create_rotating_handler(log_file: str, format: str = 'long') -> RotatingFileHandler:
    """Create a rotating file handler with size limits"""
    handler = RotatingFileHandler(
        log_file,
        maxBytes=LogConfig.MAX_BYTES,
        backupCount=LogConfig.BACKUP_COUNT,
        mode='a'
    )
    return formatted_handler(handler, format)


# /////////////////////////////////////////////////////////////////////////////
def create_console_handler(format: str = 'short') -> logging.StreamHandler:
    """Create a console handler"""
    return formatted_handler(logging.StreamHandler(), format)
  

# /////////////////////////////////////////////////////////////////////////////
def formatted_handler(handler: logging.Handler, format: str) -> logging.Handler:
    """Format a handler using predefined formats"""
    if format not in LogConfig.FORMATS:
        raise ValueError(f"Invalid format type: {format}")
    
    fmt = LogConfig.FORMATS[format]
    formatter = logging.Formatter(fmt['msg'], fmt['date'])
    handler.setFormatter(formatter)
    return handler
  

# /////////////////////////////////////////////////////////////////////////////
def log_format(format):
  """Return a logging formatter based on the specified format type."""
  
  if format == 'long':
    msg_format = '%(asctime)s - %(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
    date_format = f'%d-%m-%Y %H:%M:%S'

  if format == 'short':
    msg_format = '%(asctime)s - %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    date_format = f'%H:%M:%S'

  return logging.Formatter(msg_format, date_format)
    

# ////////////////////////////////////////////////////////////////////////////
class LoggerFactory:
    """Factory class for creating loggers"""
    _loggers: Dict[str, logging.Logger] = {}
    
    @classmethod
    def get_logger(cls, name: str, **kwargs: Any) -> logging.Logger:
        """Get or create a logger with specified configuration"""
        if name not in cls._loggers:
            cls._loggers[name] = setup_logger(name, **kwargs)
        return cls._loggers[name]


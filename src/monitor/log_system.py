# /////////////////////////////////////////////////////////////////////////////
# LOGGING SYSTEM 
#
# This module provides a logging system with configurable loggers re-usable across 
# multiple applications. It allows the creation of multiple loggers with different 
# settings within a LoggerFactory class.
#
# The module requires the following application-specific settings to be imported:
#   1. LOG_DIR: Relative path of directory to store the log files
#   2. LOG_CONFIGS: List of lists of logger configurations in the format
#           [log name, 
#           log level,
#           message length ('short' or 'long')'
#           output to console in addition to log file (boolean)]
#
# Messages sent to the console are always short format.
#
# /////////////////////////////////////////////////////////////////////////////

import logging
import os
import shutil
import atexit
from logging.handlers import RotatingFileHandler
from typing import Dict, Any
from dataclasses import dataclass
from src.config.config_logs import LOG_DIR, LOG_CONFIGS


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
    level: int,
    format: str,
    console: bool,
) -> logging.Logger:
    """Set up a logger with improved error handling"""
    
    try:
        ensure_log_directory_exists(log_file)
        logger = logging.getLogger(logger_name)
        # Clear ALL existing handlers
        logger.handlers.clear()
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
def create_rotating_handler(log_file: str, format: str) -> RotatingFileHandler:
    """Create a rotating file handler with size limits"""
    handler = RotatingFileHandler(
        log_file,
        maxBytes=LogConfig.MAX_BYTES,
        backupCount=LogConfig.BACKUP_COUNT,
        mode='w'
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
    """Factory class for creating and managing loggers"""
    _loggers: Dict[str, logging.Logger] = {}
    
    @classmethod
    def create_logger(cls, name: str, **kwargs: Any) -> logging.Logger:
        """Create a new logger with specified configuration
        
        Args:
            name: Name of the logger
            **kwargs: Configuration options including:
                log_file: Path to log file
                level: Logging level (default: INFO)
                format: Log format type (default: 'long')
                console: Enable console output (default: False)
        """
        logger = setup_logger(name, **kwargs)
        cls._loggers[name] = logger
        return logger

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Retrieve an existing logger
        
        Args:
            name: Name of the logger to retrieve
        Raises:
            KeyError: If logger doesn't exist
        """
        if name not in cls._loggers:
            raise KeyError(f"Logger '{name}' not found. Create it first using create_logger()")
        return cls._loggers[name]


# ////////////////////////////////////////////////////////////////////////////
class ApplicationLogger:
    """Manages application logging lifecycle"""
    _initialized = False
    _loggers = {}
    
    # LOG CONFIGURATION SETTINGS
    _log_dir = LOG_DIR
    _log_configs = LOG_CONFIGS
    
    @classmethod
    def initialize(cls):
        """Initialize all application loggers"""
        if cls._initialized:
            return
         
        cls.wipe_old_logs()
        
        for log in cls._log_configs:
            cls._loggers[log[0]] = LoggerFactory.create_logger(
                name=log[0],
                level=log[1],
                format=log[2],
                console=log[3],
                log_file=f'{cls._log_dir}/{log[0]}.log',
            )

        cls._initialized = True
        atexit.register(cls.cleanup)

    @classmethod
    def wipe_old_logs(cls):
        """Shutdown existing logging system and remove & remake log directory"""
        logging.shutdown()
        logging.getLogger().handlers.clear()

        if os.path.exists(cls._log_dir):
            shutil.rmtree(cls._log_dir)
        os.makedirs(cls._log_dir, exist_ok=True)
        open(os.path.join(cls._log_dir, '.gitkeep'), 'w').close()  # Create empty .gitkeep file

    @classmethod
    def cleanup(cls):
        """Cleanup logging system"""
        logging.shutdown()
        cls._initialized = False

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get a logger by name"""
        if not cls._initialized:
            cls.initialize()
        return cls._loggers[name]


# ////////////////////////////////////////////////////////////////////////////
def get_loggers():
    """Get all application loggers"""
    return tuple(ApplicationLogger.get_logger(log[0]) for log in LOG_CONFIGS)
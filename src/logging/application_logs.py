# /////////////////////////////////////////////////////////////////////////////
# APPLICATION LOGS
#  
# This module defines the logger instances used in the application, set up via 
# a LoggerFactory class.
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
from src.logging.log_system import LoggerFactory


# /////////////////////////////////////////////////////////////////////////////
def initialize_application_loggers():
    """
    Initialize application loggers with specified configurations.
    
    This function must be called once at the start of the application in order
    to set up the loggers used throughout the application.
    """
    LoggerFactory.get_logger(
        'debug',
        log_file='logs/debug.log',
        format='short',
        level=logging.DEBUG,
    )
    LoggerFactory.get_logger(
        'errors',
        log_file='logs/errors.log',
        level=logging.WARNING,
        console=True,
    )
    LoggerFactory.get_logger(
        'output',
        log_file='logs/output.log',
        level=logging.INFO,
    )

# /////////////////////////////////////////////////////////////////////////////
# Initialize loggers when module is imported
initialize_application_loggers()

# Names of logger instances to be exported for use in other modules
log_debug = LoggerFactory.get_logger('debug')
log_error = LoggerFactory.get_logger('errors')
log_output = LoggerFactory.get_logger('output')

log_output.info("Logging system initialised") 
# /////////////////////////////////////////////////////////////////////////////
# APPLICATION LOGS
#  
# This module specifies the logger instances to be used in the application.
# 
# The LOG_DIR and LOG_CONFIGS settings must be imported into the log_system module.
#
#   1. LOG_DIR: Relative path of directory to store the log files
#   2. LOG_CONFIGS: List of lists of logger configurations in the format
#           [log name, 
#           log level,
#           message length ('short' or 'long')'
#           output to console in addition to log file (boolean)]
#
# /////////////////////////////////////////////////////////////////////////////

import logging

# Relative path of directory to store the log files
LOG_DIR = 'logs'

# Logger configurations
LOG_CONFIGS = [
    ['debug', logging.DEBUG, 'short', False],
    ['errors', logging.WARNING, 'long', True],
    ['output', logging.INFO, 'long', False],
]


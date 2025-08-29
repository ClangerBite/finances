# /////////////////////////////////////////////////////////////////////////////
# CUSTOM EXCEPTIONS MODULE
# /////////////////////////////////////////////////////////////////////////////

from typing import Optional
from src.logging.log_system import get_loggers

# Get logger instances at module level
log_debug, log_error, log_output = get_loggers()


# /////////////////////////////////////////////////////////////////////////////
class BaseError(Exception):
    """Base exception class for all custom errors"""
    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        log_error.error(self._format_message(), stacklevel=2)
        super().__init__(self._format_message())
        
    def _format_message(self) -> str:
        """Format the error message with optional details"""
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


# /////////////////////////////////////////////////////////////////////////////
class FileSystemError(BaseError):
    """Base class for file system related errors"""
    pass

class DirectoryNotFoundError(FileSystemError):
    """Exception raised when directory is not found"""
    def __init__(self, directory: str):
        super().__init__(
            message=f'Directory not found',
            details=f'"{directory}"'
        )


# /////////////////////////////////////////////////////////////////////////////
class FilePathError(FileSystemError):
    """Base class for file path related errors"""
    pass

class FilePathCreationError(FilePathError):
    """Exception raised when cannot create a file path"""
    def __init__(self, item: str, directory: str, error: Exception):
        super().__init__(
            message=f"Error creating filepath for item {item} in directory {directory}",
            details=str(error)
        )

class AbsolutePathCreationError(FilePathError):
    """Exception raised when cannot create an absolute path"""
    def __init__(self, file_path: str, error: Exception):
        super().__init__(
            message=f"Error creating absolute path from relative path {file_path}",
            details=str(error)
        )


# /////////////////////////////////////////////////////////////////////////////
class FileOperationError(FileSystemError):
    """Base class for file operation errors"""
    pass

class ListFilesError(FileOperationError):
    """Exception raised when cannot list files in a directory"""
    def __init__(self, error: Exception):
        super().__init__(
            message="Error listing files",
            details=str(error)
        )

class ReadFileError(FileOperationError):
    """Exception raised when cannot read a file"""
    def __init__(self, file_path: str, error: Exception):
        super().__init__(
            message=f"Error reading file {file_path}",
            details=str(error)
        )

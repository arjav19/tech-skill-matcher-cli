class JobMatcherError(Exception):
    """Base exception for the application."""
    
    pass

class InvalidFileFormatError(JobMatcherError):
    """Raised when an unsupported file extension is provided."""

    pass

class EmptyFileError(JobMatcherError):
    """Raised when an ingested file is empty."""

    pass

class TendaError(Exception):
    """Base exception for Tenda router errors."""


class TendaConnectionError(TendaError):
    """Router could not be reached."""


class TendaAuthenticationError(TendaError):
    """Authentication failed or session is not authenticated."""


class TendaResponseError(TendaError):
    """Router returned an unexpected response."""


class TendaDataError(TendaError):
    """Router returned invalid or unexpected data."""

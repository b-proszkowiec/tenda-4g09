"""Tenda 4G09 router client."""

from .client import Tenda4G09
from .auth import Auth
from .models import *
from .models import __all__ as _models_all
from .enums import *
from .enums import __all__ as _enums_all

__all__ = [
    "Tenda4G09",
    "Auth",
    *_models_all,
    *_enums_all,
]

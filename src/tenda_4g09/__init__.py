"""Tenda 4G09 router client."""

from .client import Tenda4G09
from .models import *
from .models import __all__ as _models_all

__all__ = [
    "Tenda4G09",
    *_models_all,
]

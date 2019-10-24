"""A CLI initiative tracker in the works [NOT USABLE YET]."""
__version__ = "0.0.5"

from .initiative import InitiativeQueue
from .rfi import main

__all__ = ["main", "InitiativeQueue"]

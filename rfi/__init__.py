"""A CLI initiative tracker in the works."""
__version__ = "0.7.0"

from .initiative import InitiativeQueue
from .rfi import main

__all__ = ["main", "InitiativeQueue"]

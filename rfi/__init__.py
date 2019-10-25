"""A CLI initiative tracker in the works."""
__version__ = "0.2.1"

from .initiative import InitiativeQueue
from .rfi import main

__all__ = ["main", "InitiativeQueue"]

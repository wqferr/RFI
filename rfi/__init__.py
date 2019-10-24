"""A CLI initiative tracker in the works."""
__version__ = "0.1.2"

from .initiative import InitiativeQueue
from .rfi import main

__all__ = ["main", "InitiativeQueue"]

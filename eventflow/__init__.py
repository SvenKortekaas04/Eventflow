"""
Eventflow provides functionalities for event-based applications. It's lightweight 
and built with simplicity and elegance in mind. Therefore, Eventflow should be 
easy to learn. It is written in pure Python and has no external dependencies.
"""

from .bus import EventBus, Event

__all__ = ("EventBus", "Event", "__version__")

MAJOR_VERSION = 0
MINOR_VERSION = 1
PATCH_VERSION = 0

__version__ = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}"
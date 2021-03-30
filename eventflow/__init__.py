"""
Eventflow provides functionalities for event-based applications. It's lightweight 
and built with simplicity and elegance in mind. Therefore, Eventflow should be 
easy to learn.

.. codeauthor:: Sven Kortekaas
"""

from .bus import EventBus, Event
from .version import __version__

__all__ = ("EventBus", "Event", "__version__")
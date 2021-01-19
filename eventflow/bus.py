from collections import defaultdict
import datetime
from typing import (
    Callable,
    Dict,
    Optional
)


class Event:
    """
    The ``Event`` class represents an event in the event bus. 

    It contains the associated event type, as well as optional 
    data and a timestamp when the event was fired.

    A simple ``dict`` is used to store optional data.

    :param event_type: The type of event.
    :type event_type: str
    :param data: The data sent with the event.
    :type data: dict
    :param timestamp: The timestamp when the event was fired.
    :type timestamp: datetime.datetime.now
    """

    def __init__(self, event_type: str, data: Optional[Dict] = {}, timestamp: Optional[datetime.datetime.now] = datetime.datetime.now(tz=datetime.timezone.utc)) -> None:
        """
        Initialize a new event object.
        """

        self.event_type = event_type
        self.data = data
        self.timestamp = timestamp

    def __repr__(self) -> str:
        """
        Return the representation.
        """

        args = [
            "event_type={}".format(self.event_type),
            "data={}".format(self.data),
            "timestamp={}".format(self.timestamp),
        ]
        
        return "<{} {}>".format(type(self).__name__, ", ".join(args))

    def as_dict(self) -> Dict:
        """
        Return dict representation of an event.
        """

        return {
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp
        }


class EventBus:
    """
    The main class of Eventflow.

    The `EventBus` class is responsible for the firing and listening of events.

    For event management, a ``dict`` is used to store the event type 
    with a list of listeners associated to the event type. The listeners 
    are accessible via the name of the event type.
    """

    def __init__(self) -> None:
        """
        Create a new EventBus instance.
        """

        self._events = defaultdict(list)

    def __len__(self) -> int:
        """
        Returns the total number of events currently in the event bus.

        :return: The sum of all events in the event bus.
        :rtype: int

        >>> len(bus)
        0
        """

        return sum(len(value) for value in self._events.values())

    def __repr__(self) -> str:
        """
        Return the representation.
        """

        args = [
            "events={}".format(len(self._events)),
        ]
        
        return "<{} {}>".format(type(self).__name__, ", ".join(args))

    @property
    def listeners(self) -> Dict[str, int]:
        """
        Returns a dictionary with events and the number of listeners.

        :return: A dictionary with events and the number of listeners
        :rtype: Dict[str, int]

        >>> bus.listeners
        {"test": 1}
        """

        return {event_type: len(listeners) for event_type, listeners in self._events.items()}

    def add_listener(self, event_type: str, listener: Callable) -> None:
        """
        Add a listener to a specific event type.

        :param event_type: The type of event
        :type event_type: str
        :param listener: A function
        :type listener: Callable
        """

        self._events[event_type].append(listener)

    def remove_listener(self, event_type: str, listener: Callable) -> None:
        """
        Remove a listener of a specific event type.

        :param event_type: The type of event
        :type event_type: str
        :param listener: A function
        :type listener: Callable
        """

        self._events[event_type].remove(listener)

    def listen(self, event_type: str) -> Callable:
        """
        Listen for events of a specific type.

        :param event_type: The type of event
        :type event_type: str
        :return: decorator function
        :rtype: Callable

        This function can be applied as follows::

            @bus.listen(event_type="...")
            def funcname(event):
                ...
        """        

        def decorator(f):
            self._events[event_type].append(f)
            return f

        return decorator
    
    def fire(
        self,
        event_type: str,
        data: Optional[Dict] = {},
        timestamp: Optional[datetime.datetime.now] = datetime.datetime.now(tz=datetime.timezone.utc)
    ) -> None:
        """
        Fire an event. This will fire every listener. Synchronous.

        :param event_type: The type of event
        :type event_type: str
        :param data: The data sent with the event, defaults to {}
        :type data: Optional[Dict], optional
        :param timestamp: The timestamp when the event was fired, defaults to datetime.datetime.now(tz=datetime.timezone.utc)
        :type timestamp: Optional[datetime.datetime.now], optional
        """

        # Create an `Event` object
        _event = Event(event_type, data, timestamp)

        for f in self._events[event_type]:
            f(event=_event.as_dict())
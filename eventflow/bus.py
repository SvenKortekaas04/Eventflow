from collections import defaultdict
import datetime
import pytz
from typing import (
    Callable,
    Dict,
    List,
    Optional
)


class Event:
    """
    The `Event` class represents an event in the event bus. 

    An `Event` object consists of metadata, data about data, and optional data. The 
    metadata comprises an event type, which indicates to what type of event it belongs, 
    and a timestamp, which indicates the exact date and time the event was fired. The 
    timestamp is set according to the UTC time zone.

    .. admonition:: Event structure

        An event is constructed and modeled to an event structure in JSON format like this:

        .. code-block:: json

            {
                "metadata": {
                    "event_type": "...",
                    "timestamp": "..."
                },
                "data": {}
            }

    .. admonition:: Customization

        For customization, the following class variables can be set:
        
        - ``default_timezone``. Defines the The timezone that is used by default to create a timestamp for the specific event.

    :param event_type: The type of event.
    :type event_type: str
    :param data: The data sent with the event.
    :type data: dict
    """

    # The timezone that is used by default to 
    # create a timestamp for the specific event
    default_timezone: str = pytz.utc.zone

    def __init__(self, event_type: str, data: Optional[Dict] = {}) -> None:
        """
        Initialize a new event object.
        """

        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.datetime.now(tz=pytz.timezone(self.default_timezone))

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
            "metadata": {
                "event_type": self.event_type,
                "timestamp": self.timestamp
            },
            "data": self.data
        }


class EventBus:
    """
    The main class of Eventflow.

    The `EventBus` class is responsible for the firing and listening of events.

    For event management, a ``dict`` is used to store the event type 
    with a list of listeners associated to the event type. The listeners 
    are accessible via the name of the event type.

    .. admonition:: Customization

        For customization, the following class variables can be set:
        
        - ``event_class``. Defines the class that will be used to create event instances.
    """

    # The class that will be used to create event instances
    event_class = Event

    def __init__(self) -> None:
        """
        Create a new EventBus instance.
        """

        self._events = defaultdict(list)  # type: Dict[Any, List[Callable]]

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

    def append(self, event_type: str, listener: Callable) -> None:
        """
        Append a listener to a specific event type.

        :param event_type: The type of event
        :type event_type: str
        :param listener: A function
        :type listener: Callable
        """

        self._events[event_type].append(listener)

    def remove(self, event_type: str, listener: Callable) -> None:
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
        data: Optional[Dict] = {}
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
        _event = Event(event_type, data)

        for f in self._events[event_type]:
            f(event=_event.as_dict())

    def fire_multiple(
        self,
        event_types: List[str],
        data: Optional[Dict] = {}
    ) -> None:
        """
        Fire multiple events. This will fire every listener. Synchronous.

        :param event_types: The types of events
        :type event_types: List[str]
        :param data: The data sent with the event, defaults to {}
        :type data: Optional[Dict], optional
        :param timestamp: The timestamp when the event was fired, defaults to datetime.datetime.now(tz=datetime.timezone.utc)
        :type timestamp: Optional[datetime.datetime.now], optional
        :raises ValueError: If the argument `event_types` is of the wrong type.
        """

        if not isinstance(event_types, List):
            raise ValueError("Argument `event_types` must be of type list.")

        for event_type in event_types:
            # Create an `Event` object
            _event = Event(event_type, data)

            for f in self._events[event_type]:
                f(event=_event.as_dict())

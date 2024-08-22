from typing import Iterator, Union, List
from buspy._event import Event
from buspy.exception import (
    EventsCollectorEventTypeError,
    EventsCollectorTypeError,
)


class EventsCollector:
    """
    A class to collect and manage events.

    Example:
        ```python
            from eventbus import EventsCollector, Event

            class UserEvents(Event):
                pass

            collector = EventsCollector()

            collector.add_event(UserEvents())
            collector.add_event(UserEvents(data={"id": 1}))
            collector.add_event(UserEvents(metadata={"id": 1}))
            collector.add_event(UserEvents(data={"id": 1}, metadata={"id": 1}))

            print(collector.pull_all_events())
            print(collector)

            for event in collector:
                print(event)

        ```
    """

    __slots__ = ["_events"]

    def __init__(self) -> None:
        """
        Initializes the EventsCollector with an empty list of events.

        Example:
        ```python
            from eventbus import EventsCollector, Event

            class UserEvents(Event):
                pass

            collector = EventsCollector()

            collector.add_event(UserEvents())
            collector.add_event(UserEvents(data={"id": 1}))
            collector.add_event(UserEvents(metadata={"id": 1}))
            collector.add_event(UserEvents(data={"id": 1}, metadata={"id": 1}))

            print(collector.pull_all_events())
            print(collector)

            for event in collector:
                print(event)

        ```

        """
        self._events: List[Event] = []

    def pull_all_events(self) -> List[Event]:
        """
        Retrieves all collected events.

        Returns:
            List[Event]: A list of all collected events.
        """
        return self._events

    def add_event(self, event: Event) -> None:
        """
        Adds an event to the collection.

        Args:
            event (Event): The event to add.

        Raises:
            EventsCollectorEventTypeError: If the event parameter is not an instance of Event.
        """
        if not isinstance(event, Event):
            raise EventsCollectorEventTypeError(event)
        self._events.append(event)

    def __getitem__(self, key: Union[slice, int]) -> Union[List[Event], Event]:
        """
        Retrieves one or more events based on the provided key.

        Args:
            key (Union[slice, int]): The index or slice to retrieve events.

        Raises:
            TypeError: If the key is not an integer or a slice.

        Returns:
            Union[list[Event], Event]: A single event or a list of events.
        """
        if isinstance(key, slice):
            return self._events[key.start : key.stop : key.step]
        if isinstance(key, int):
            return self._events[key]
        raise EventsCollectorTypeError(key)

    def __iter__(self) -> Iterator[Event]:
        """
        Returns an iterator over the collected events.

        Returns:
            Iterator[Event]: An iterator over the collected events.
        """
        return iter(self._events)

    def __repr__(self) -> str:
        """
        Returns a string representation of the EventsCollector.

        Returns:
            str: A string representation of the collected events.
        """
        return repr(self._events)

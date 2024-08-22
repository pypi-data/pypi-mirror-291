import json
import os
from typing import Callable, Set, Any, Dict, List, Union
import inspect
from pyee import EventEmitter
from buspy._event import Event
from buspy._events_collector import EventsCollector
from buspy.exception import (
    EventBusEventTypeError,
    EventBusHandlerTypeError,
    EventBusHandlerSignatureError,
)


class EventBus:
    """A class to manage event-driven programming using an event bus."""

    __slots__ = [
        "_event_bus",
        "_events",
    ]

    def __init__(self) -> None:
        """
        Initializes the EventBus.

        Example:
        ```python
            from eventbus import EventBus, EventsCollector, Event

            class UserEvent(Event):
                pass

            class CreatedUserEvent(UserEvent):
                pass

            event_bus = EventBus()

            def handler_all_event(event: Event) -> None:
                print(event)

            def handler_user_event(event: Event) -> None:
                handler_all_event(event)

            def handler_created_user_event(event: Event) -> None:
                handler_all_event(event)

            event_bus.add_listener(handler=handler_all_event, event=Event())
            event_bus.add_listener(handler=handler_user_event, event=UserEvent())
            event_bus.add_listener(handler=handler_created_user_event, event=CreatedUserEvent())


            event_bus.emit(Event(data={"demo_event": 1}))
            event_bus.emit(UserEvent(data={"demo_user_event": 1}))
            event_bus.emit(CreatedUserEvent(data={"demo_created_user_event": 1}))


            collector = EventsCollector()
            collector.add_event(Event(data={"demo_event": 1}))
            collector.add_event(UserEvent(data={"demo_user_event": 1}))
            collector.add_event(CreatedUserEvent(data={"demo_created_user_event": 1}))

            event_bus.emit(collector)

            print(event_bus.event_names())
            print(event_bus.listeners(event=CreatedUserEvent()))
            print(event_bus.summary())

        ```
        """
        self._event_bus = EventEmitter()
        self._events: Dict[str, Event] = {}

    def emit(
        self, event: Union[Event, EventsCollector], strict_event: bool = False
    ) -> None:
        """
        Emits an event to the event bus.

        Args:
            event (Union[Event, EventsCollector]): The event or events to emit.
            strict_event (bool): If True, only emit the event if the event name matches exactly.
                                 If False, emit the event if the event name contains the key.
        Raises:
            TypeError: If the event is not an instance of Event.
        """
        if not isinstance(event, (Event, EventsCollector)):
            raise EventBusEventTypeError(event)

        if isinstance(event, Event):
            self._emit(event, strict_event)

        if isinstance(event, EventsCollector):
            for _event in event:
                self._emit(_event, strict_event)

    def _emit(self, event: Event, strict_event: bool) -> None:
        if strict_event is False:
            for key in self._events:
                if key in event.event_name:
                    self._event_bus.emit(key, event)

        elif strict_event is True:
            self._event_bus.emit(event.event_name, event)

    def add_listener(self, event: Event, handler: Callable[[Event], Any]) -> None:
        """
        Adds a listener for a specific event.

        Args:
            event (Event): The event to listen for.
            handler (Callable[[Event], Any]): The handler function to call when the event is emitted.
        Raises:
            TypeError: If the event is not an instance of Event or the handler is not callable.
            ValueError: If the handler does not accept exactly one parameter or the parameter is not of type Event.
        """
        if not isinstance(event, Event):
            raise EventBusEventTypeError(event)
        if not isinstance(handler, Callable):  # type: ignore
            raise EventBusHandlerTypeError(handler)

        sig = inspect.signature(handler)

        if len(sig.parameters) != 1:
            raise EventBusHandlerSignatureError(handler)
        param = next(iter(sig.parameters.values()))

        if param.annotation is not Event:
            raise EventBusHandlerSignatureError(handler)

        self._event_bus.add_listener(event.event_name, handler)
        self._events[event.event_name] = event

    def event_names(self) -> Set[str]:
        """
        Returns a set of all event names.

        Returns:
            Set[str]: A set of event names.
        """
        return self._event_bus.event_names()

    def listeners(self, event: Event) -> Dict[str, List[str]]:
        """
        Returns a dictionary of listeners for a specific event.

        Args:
            event (Event): The event to get listeners for.
        Raises:
            TypeError: If the event is not an instance of Event.
        Returns:
            dict[str, list[str]]: A dictionary with the event name as the key and a list of listeners as the value.
        """
        if not isinstance(event, Event):
            raise EventBusEventTypeError(event)

        _response = []
        listeners = self._event_bus.listeners(event.event_name)
        for listener in listeners:
            source_file = inspect.getsourcefile(listener)
            source_line = inspect.getsourcelines(listener)
            file_name = os.path.basename(source_file) if source_file else "unknown"
            name = listener.__name__
            _response.append(f"{name}: {file_name}:{source_line[1]}")

        return {event.event_name: _response}

    def summary(self) -> str:
        """
        Returns a summary of all events and their listeners in JSON format.

        Returns:
            str: A JSON string summarizing all events and their listeners.
        """
        _event_names = self.event_names()
        _response = []
        for event_name in set(_event_names):
            _response.append(self.listeners(self._events.get(event_name)))  # type: ignore
        return json.dumps(_response, indent=2)

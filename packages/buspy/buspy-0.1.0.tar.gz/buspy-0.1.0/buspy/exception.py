from typing import Any


class EventsCollectorEventTypeError(TypeError):
    """
    Exception raised when the 'event' parameter is not a valid type.

    Attributes:
        event: The invalid data that caused the exception.
    """

    def __init__(self, event: Any):  # noqa
        super().__init__(
            f"\n\tThe 'event' parameter is of type '{type(event)}' and must be of type 'Event'"
        )


class EventsCollectorTypeError(TypeError):
    """
    Exception raised when the 'key' parameter is not a valid type.

    Attributes:
        key: The invalid data that caused the exception.
    """

    def __init__(self, key: Any):  # noqa
        super().__init__(
            f"\n\tEventsCollector indices must be integers or slices, not {type(key)}."
        )


class EventDataTypeError(TypeError):
    """
    Exception raised when the 'data' parameter is not a valid type.

    Attributes:
        data: The invalid data that caused the exception.
    """

    def __init__(self, data: Any):  # noqa
        super().__init__(
            f"\n\tThe 'data' parameter is of type '{type(data)}' and must be of type 'dict' or None."
        )


class EventMetadataTypeError(TypeError):
    """
    Exception raised when the 'metadata' parameter is not a valid type.

    Attributes:
        metadata: The invalid metadata that caused the exception.
    """

    def __init__(self, metadata: Any):  # noqa
        super().__init__(
            f"\n\tThe 'metadata' parameter is of type '{type(metadata)}' and must be of type 'dict' or None."
        )


class EventDataItemsTypeError(TypeError):
    """
    Exception raised when the 'data' parameter contains items not serializable to JSON.

    Attributes:
        data: The invalid data that caused the exception.
    """

    def __init__(self, data: Any):  # noqa
        super().__init__(
            f"\n\tThe 'data' must be a JSON serializable (dict[str, Union[str, int, float, bool, None]]).\n\tdata: {data}'"
        )


class EventMetadataItemsTypeError(TypeError):
    """
    Exception raised when the 'metadata' parameter contains items not serializable to JSON.

    Attributes:
        metadata: The invalid metadata that caused the exception.
    """

    def __init__(self, metadata: Any):  # noqa
        super().__init__(
            f"\n\tThe 'metadata' must be a JSON serializable (dict[str, Union[str, int, float, bool, None]]).\n\tdata: {metadata}'"
        )


class EventRootValueError(ValueError):
    """
    Exception raised when the root class of an event is not 'Event'.

    Attributes:
        data: The name of the root class that caused the exception.
    """

    def __init__(self, data: str):  # noqa
        super().__init__(
            f"\n\tThe root class is '{data}' and should be the Event class. (from event_bus import Event)"
        )


class UnexpectedError(Exception):
    """Exception raised for unexpected errors in the event logic."""


class EventBusEventTypeError(TypeError):
    """
    Exception raised when the 'event' parameter is not a valid type.

    Attributes:
        event: The invalid data that caused the exception.
    """

    def __init__(self, event: Any):  # noqa
        super().__init__(
            f"\n\tThe 'event' parameter is of type '{type(event)}' and must be of type 'Event'"
        )


class EventBusHandlerTypeError(TypeError):
    """
    Exception raised when the 'event' parameter is not a valid type.

    Attributes:
        event: The invalid data that caused the exception.
    """

    def __init__(self, handler: Any):  # noqa
        super().__init__(
            f"\n\tThe 'handler' parameter is of type '{type(handler)}' and must be of type 'Callable'"
        )


class EventBusHandlerSignatureError(TypeError):
    """
    Exception raised when the 'event' parameter is not a valid type.

    Attributes:
        event: The invalid data that caused the exception.
    """

    def __init__(self, handler: Any):  # noqa
        super().__init__(
            f"\n\tThe 'handler' parameter is of type '{type(handler)}' and must be of type 'Callable'"
        )

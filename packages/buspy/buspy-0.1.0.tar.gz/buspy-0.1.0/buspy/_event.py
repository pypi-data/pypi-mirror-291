import os
from typing import Any, Union, Optional, Dict
from datetime import datetime, timezone
from uuid import uuid4
import json
import inspect
from buspy.exception import (
    EventDataTypeError,
    EventMetadataTypeError,
    EventDataItemsTypeError,
    EventMetadataItemsTypeError,
    EventRootValueError,
    UnexpectedError,
)


class Event:
    """
    A class representing an event with associated data and metadata.

    Attributes:
        data (Optional[dict]): The event data.
        metadata (Optional[dict]): The event metadata.
        event_id (str): A unique identifier for the event.
        created_at (str): The timestamp when the event was created.
    """

    __slots__ = [
        "_event_name",
        "_event_id",
        "_created_at",
        "_data",
        "_metadata",
        "_source",
    ]

    def __init__(
        self,
        data: Optional[Dict[str, Union[str, int, float, bool, None]]] = None,
        metadata: Optional[Dict[str, Union[str, int, float, bool, None]]] = None,
    ) -> None:
        """
        Initializes an Event instance with specified data and metadata.

        Parameters:
            data (Optional[dict]): The event data.
            metadata (Optional[dict]): The event metadata.

        Raises:
            EventDataTypeError: If the data parameter is not a dictionary or None.
            EventMetadataTypeError: If the metadata parameter is not a dictionary or None.
            EventDataItemsTypeError: If the data contains non-serializable items.
            EventMetadataItemsTypeError: If the metadata contains non-serializable items.
            EventRootValueError: If the class hierarchy does not start with 'Event'.
            UnexpectedError: For any unexpected conditions in class hierarchy validation.
        """
        if data is not None and not isinstance(data, dict):
            raise EventDataTypeError(data=data)

        if metadata is not None and not isinstance(metadata, dict):
            raise EventMetadataTypeError(metadata=metadata)

        try:
            self._data = json.loads(json.dumps(data))
        except TypeError as error:
            raise EventDataItemsTypeError(data=data) from error

        try:
            self._metadata = json.loads(json.dumps(metadata))
        except TypeError as error:
            raise EventMetadataItemsTypeError(metadata=metadata) from error

        self._event_name = self._check_and_generate_event_name()

        self._created_at = str(datetime.now(timezone.utc).isoformat())

        self._event_id = str(uuid4())

        self._source = self._caller

    def _check_and_generate_event_name(self) -> str:
        """
        Checks the hierarchy of the class and generates an event name.

        Returns:
            str: The generated event name.

        Raises:
            EventRootValueError: If the hierarchy does not start with 'Event'.
            UnexpectedError: If the current class name does not match the expected.
        """
        _current_class = self.__class__
        _hierarchy = []
        while _current_class.__name__ != "object":
            _hierarchy.append(_current_class.__name__)
            bases = _current_class.__bases__
            _current_class = bases[0] if bases else None  # type: ignore[assignment]
            if not _current_class:
                break
        _hierarchy = _hierarchy[::-1]

        if _hierarchy[0] != "Event":
            raise EventRootValueError(_hierarchy[0])

        if _hierarchy[-1] != self.__class__.__name__:
            raise UnexpectedError(f"{_hierarchy[-1]} != {self.__class__.__name__}")

        return ".".join(_hierarchy)

    @property
    def event_name(self) -> str:
        """
        Returns the name of the event.

        Returns:
            str: The name of the event.
        """
        return self._event_name

    @property
    def event_id(self) -> str:
        """
        Returns the unique identifier of the event.

        Returns:
            str: The unique identifier of the event.
        """
        return self._event_id

    @property
    def created_at(self) -> str:
        """
        Returns the timestamp when the event was created.

        Returns:
            str: The creation timestamp of the event.
        """
        return self._created_at

    @property
    def data(self) -> Optional[Dict[str, Union[str, int, float, bool, None]]]:
        """
        Returns the event data.

        Returns:
            Optional[dict]: The event data, or None if not set.
        """
        return self._data

    @property
    def metadata(self) -> Optional[Dict[str, Union[str, int, float, bool, None]]]:
        """
        Returns the event metadata.

        Returns:
            Optional[dict]: The event metadata, or None if not set.
        """
        return self._metadata

    def __setattr__(self, __name: str, __value: Any) -> None:
        """None"""
        if __name not in self.__slots__:
            raise AttributeError(f"Unable to set the '{__name}' attribute at runtime.")
        try:
            self.__getattribute__(__name)
        except AttributeError:
            super().__setattr__(__name, __value)
            return
        raise AttributeError(f"Unable to set the '{__name}' attribute at runtime.")

    @property
    def _caller(self) -> str:
        """
        Attempts to retrieve the caller's file and line number.

        Returns:
            str: A string representing the caller's file and line number, or an empty string if not available.
        """
        try:
            frame = inspect.currentframe().f_back.f_back  # type: ignore[union-attr]
            line = frame.f_lineno  # type: ignore[union-attr]
            file_path = frame.f_globals["__file__"]  # type: ignore[union-attr]
            file_name = os.path.basename(file_path)
            return f"{file_name}:{str(line)}"
        except Exception:  # pylint: disable=broad-exception-caught
            return ""

    def __eq__(self, other: object) -> bool:
        """
        Checks for equality between two Event instances.

        Parameters:
            other (object): The object to compare.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        return isinstance(other, Event) and self.__hash__() == other.__hash__()

    def __str__(self) -> str:
        """
        Returns a string representation of the Event instance.

        Returns:
            str: A formatted string representing the event.
        """
        return f"{self.event_name}:\n\tdata = {str(self.data)}\n\tevent_id = {self.event_id}\n\tcreated_at = {str(self.created_at)}\n\tmetadata = {str(self.metadata)}\n\tsource = {self._source}\n"

    def __hash__(self) -> int:
        """
        Returns a hash value of the Event instance based on its event ID.

        Returns:
            int: The hash value of the event.
        """
        return hash(self.event_id)

    def __repr__(self) -> str:
        """
        Provides the official string representation of the Event instance.

        Returns:
            str: A string representation suitable for debugging.
        """
        return (
            f"{self.__class__.__name__}(data = {self.data}, metadata = {self.metadata})"
        )

    def to_dict(self) -> dict:
        """
        Converts the Event instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the event details.
        """
        _data = {
            "event_name": self.event_name,
            "data": self.data,
            "event_id": self.event_id,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }
        return _data

    def to_json(self) -> str:
        """
        Converts the Event instance to a JSON string representation.

        Returns:
            str: A JSON string representing the event details.
        """
        return json.dumps(self.to_dict(), indent=2)

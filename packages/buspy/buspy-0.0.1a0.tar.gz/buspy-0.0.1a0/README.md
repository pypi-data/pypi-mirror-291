# EventBus Python Library

## Overview
The EventBus Python Library provides a structured way to work with events within your application. It consists of three main components:

1. **EventBus**: Manages event emission and listener registration.
2. **Event**: Represents an event with data and metadata.
3. **EventsCollector**: Collects and manages a list of events.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Creating an Event](#creating-an-event)
  - [Using EventBus](#using-eventbus)
  - [Collecting Events](#collecting-events)
- [Contributing](#contributing)
- [License](#license)

## Installation
You can install this library using pip:
```bash
pip install eventbus
``````


## Usage

### Creating an Event

First, you need to import the `Event` class and create an event instance:

```python
from eventbus import Event

#create a generic event
event = Event(data={"key": "value"},
              metadata={"source": "example"})

#define a custom event.
class UserEvent(Event):
    pass

class CreatedUserEvent(UserEvent):
    pass

user_event = UserEvent(data={"id": "123456"})
created_user_event = CreatedUserEvent(data={"id": "123456"})

print(event)
print(user_event)
print(created_user_event)
```
Resultado:
```bash
Event:
        data = {'key': 'value'}
        event_id = f9fa5ee8-d4f9-4240-b73b-031dae0092bc
        created_at = 2024-08-12T18:57:16.642223+00:00
        metadata = {'source': 'example'}
        source = file.py:4

Event.UserEvent:
        data = {'id': '123456'}
        event_id = 36a28674-46e4-4aab-8e13-8106d79ae865
        created_at = 2024-08-12T18:57:16.642451+00:00
        metadata = None
        source = file.py:15

Event.UserEvent.CreatedUserEvent:
        data = {'id': '123456'}
        event_id = 1ddd0af3-9fcb-4eb0-98fb-b42b118d35f3
        created_at = 2024-08-12T18:57:16.642479+00:00
        metadata = None
        source = file.py:16

```

Tambien se admite to_dict() y to_json() para trasmitir eventos.

```python
from eventbus import Event

#define a custom event "UserEvent"
class UserEvent(Event):
    pass

#define a custom event "CreatedUserEvent"
class CreatedUserEvent(UserEvent):
    pass

created_user_event = CreatedUserEvent(data={"id": "123456"})

print("dict:")
print(created_user_event.to_dict())
print()
print("json:")
print(created_user_event.to_json())
```
Resultado:
```bash
dict:
{'event_name': 'Event.UserEvent.CreatedUserEvent', 'data': {'id': '123456'}, 'event_id': '742c38fa-51e1-4eb8-879b-9dfe4d07de0a', 'created_at': '2024-08-12T19:02:13.542163+00:00', 'metadata': None}

json:
{
  "event_name": "Event.UserEvent.CreatedUserEvent",
  "data": {
    "id": "123456"
  },
  "event_id": "742c38fa-51e1-4eb8-879b-9dfe4d07de0a",
  "created_at": "2024-08-12T19:02:13.542163+00:00",
  "metadata": null
}
```

### Collecting Events

To collect and manage events, use the `EventsCollector` class:
```python
from eventbus import EventsCollector, Event, EventBus

# Initialize EventsCollector
collector = EventsCollector()

#define a custom event "UserEvent"
class UserEvent(Event):
    pass

#define a custom event "CreatedUserEvent"
class CreatedUserEvent(UserEvent):
    pass

# Create an event
user_event = UserEvent(data={"key": "value"}, metadata={"source": "example"})

created_user_event1 = CreatedUserEvent(data={"id": 123456}, metadata={"source": "example"})

created_user_event2 = CreatedUserEvent(data={"id": 789123}, metadata={"source": "example"})


# Add event to collector
collector.add_event(user_event)
collector.add_event(created_user_event1)
collector.add_event(created_user_event2)

# Retrieve all events
events = collector.pull_all_events()
print("First print:")
print(events)

print()
print("Second print:")
for event in collector:
    print(event)

print()
print("Therty print:")
print(collector[0])
```
Resultado:
```bash
First print:
[UserEvent(data = {'key': 'value'}, metadata = {'source': 'example'}), CreatedUserEvent(data = {'id': 123456}, metadata = {'source': 'example'}), CreatedUserEvent(data = {'id': 789123}, metadata = {'source': 'example'})]

Second print:
Event.UserEvent:
        data = {'key': 'value'}
        event_id = af4e1637-b145-4da7-a92b-53d8306ec22d
        created_at = 2024-08-12T19:09:44.386102+00:00
        metadata = {'source': 'example'}
        source = prueba.py:15

Event.UserEvent.CreatedUserEvent:
        data = {'id': 123456}
        event_id = 65dc0b38-4990-4b96-b532-8d46bdc472d5
        created_at = 2024-08-12T19:09:44.386322+00:00
        metadata = {'source': 'example'}
        source = prueba.py:17

Event.UserEvent.CreatedUserEvent:
        data = {'id': 789123}
        event_id = 283a4b51-4894-42ec-95d7-2365ee67e06e
        created_at = 2024-08-12T19:09:44.386351+00:00
        metadata = {'source': 'example'}
        source = prueba.py:19


Therty print:
Event.UserEvent:
        data = {'key': 'value'}
        event_id = af4e1637-b145-4da7-a92b-53d8306ec22d
        created_at = 2024-08-12T19:09:44.386102+00:00
        metadata = {'source': 'example'}
        source = prueba.py:15
```

### Using EventBus

To manage and emit events, use the `EventBus` class:

```python
from eventbus import EventBus, EventsCollector, Event

class UserEvent(Event):
    pass

class CreatedUserEvent(UserEvent):
    pass

event_bus = EventBus()

def handler_all_event(event: Event) -> None:
    print("Print from handler_all_event")
    print(event)

def handler_user_event(event: Event) -> None:
    print("Print from handler_user_event")
    print(event)

def handler_created_user_event(event: Event) -> None:
    print("Print from handler_created_user_event")
    print(event)

event_bus.add_listener(handler=handler_all_event, event=Event())
event_bus.add_listener(handler=handler_user_event, event=UserEvent())
event_bus.add_listener(handler=handler_created_user_event, event=CreatedUserEvent())

print()
print("Print Emit Event")
event_bus.emit(Event(data={"demo_event": 1}))
event_bus.emit(UserEvent(data={"demo_user_event": 1}))
event_bus.emit(CreatedUserEvent(data={"demo_created_user_event": 1}))

collector = EventsCollector()
collector.add_event(Event(data={"demo_event": 1}))
collector.add_event(UserEvent(data={"demo_user_event": 1}))
collector.add_event(CreatedUserEvent(data={"demo_created_user_event": 1}))

print()
print("Print Emit Collector")
event_bus.emit(collector)

print()
print("Print Event Names")
print(event_bus.event_names())

print()
print("Print Listeners")
print(event_bus.listeners(event=CreatedUserEvent()))

print()
print("Print Summary")
print(event_bus.summary())
```
Resultado:
```bash
Print Emit Event
Print from handler_all_event
Event:
        data = {'demo_event': 1}
        event_id = 9f260a1e-b999-484d-b1ec-6b77a7136128
        created_at = 2024-08-12T19:30:40.492722+00:00
        metadata = None
        source = file.py:29

Print from handler_all_event
Event.UserEvent:
        data = {'demo_user_event': 1}
        event_id = 926679fd-e19a-4b8a-8baf-92b0291c71e2
        created_at = 2024-08-12T19:30:40.492770+00:00
        metadata = None
        source = file.py:30

Print from handler_user_event
Event.UserEvent:
        data = {'demo_user_event': 1}
        event_id = 926679fd-e19a-4b8a-8baf-92b0291c71e2
        created_at = 2024-08-12T19:30:40.492770+00:00
        metadata = None
        source = file.py:30

Print from handler_all_event
Event.UserEvent.CreatedUserEvent:
        data = {'demo_created_user_event': 1}
        event_id = 931e4b6a-17da-4dc3-aff0-05b97362639f
        created_at = 2024-08-12T19:30:40.492826+00:00
        metadata = None
        source = file.py:31

Print from handler_user_event
Event.UserEvent.CreatedUserEvent:
        data = {'demo_created_user_event': 1}
        event_id = 931e4b6a-17da-4dc3-aff0-05b97362639f
        created_at = 2024-08-12T19:30:40.492826+00:00
        metadata = None
        source = file.py:31

Print from handler_created_user_event
Event.UserEvent.CreatedUserEvent:
        data = {'demo_created_user_event': 1}
        event_id = 931e4b6a-17da-4dc3-aff0-05b97362639f
        created_at = 2024-08-12T19:30:40.492826+00:00
        metadata = None
        source = file.py:31


Print Emit Collector
Print from handler_all_event
Event:
        data = {'demo_event': 1}
        event_id = 157dfcb9-fd84-4491-b2f4-a055ebd6e687
        created_at = 2024-08-12T19:30:40.492893+00:00
        metadata = None
        source = file.py:34

Print from handler_all_event
Event.UserEvent:
        data = {'demo_user_event': 1}
        event_id = bf40106c-922f-4de1-9632-f02c2baa6809
        created_at = 2024-08-12T19:30:40.492911+00:00
        metadata = None
        source = file.py:35

Print from handler_user_event
Event.UserEvent:
        data = {'demo_user_event': 1}
        event_id = bf40106c-922f-4de1-9632-f02c2baa6809
        created_at = 2024-08-12T19:30:40.492911+00:00
        metadata = None
        source = file.py:35

Print from handler_all_event
Event.UserEvent.CreatedUserEvent:
        data = {'demo_created_user_event': 1}
        event_id = 5a4ed322-3d35-48bb-bc84-cb3837bc1fae
        created_at = 2024-08-12T19:30:40.492928+00:00
        metadata = None
        source = file.py:36

Print from handler_user_event
Event.UserEvent.CreatedUserEvent:
        data = {'demo_created_user_event': 1}
        event_id = 5a4ed322-3d35-48bb-bc84-cb3837bc1fae
        created_at = 2024-08-12T19:30:40.492928+00:00
        metadata = None
        source = file.py:36

Print from handler_created_user_event
Event.UserEvent.CreatedUserEvent:
        data = {'demo_created_user_event': 1}
        event_id = 5a4ed322-3d35-48bb-bc84-cb3837bc1fae
        created_at = 2024-08-12T19:30:40.492928+00:00
        metadata = None
        source = file.py:36


Print Event Names
{'Event.UserEvent', 'Event.UserEvent.CreatedUserEvent', 'Event'}

Print Listeners
{'Event.UserEvent.CreatedUserEvent': ['handler_created_user_event: file.py:19']}

Print Summary
[
  {
    "Event.UserEvent": [
      "handler_user_event: file.py:15"
    ]
  },
  {
    "Event.UserEvent.CreatedUserEvent": [
      "handler_created_user_event: file.py:19"
    ]
  },
  {
    "Event": [
      "handler_all_event: file.py:11"
    ]
  }
]
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request to improve the library.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

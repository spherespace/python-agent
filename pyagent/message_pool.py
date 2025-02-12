import json
from queue import Queue
from threading import Lock

from .filter import Filters

from .config import Config
from .message_type import RelayMessageType
from .event import Event

class EventMessage:
    def __init__(self, event: Event, subscription_id: str, url: str) -> None:
        self.event = event
        self.subscription_id = subscription_id
        self.url = url

class NoticeMessage:
    def __init__(self, content: str, url: str) -> None:
        self.content = content
        self.url = url

class EndOfStoredEventsMessage:
    def __init__(self, subscription_id: str, url: str) -> None:
        self.subscription_id = subscription_id
        self.url = url

class MessagePool:
    def __init__(self,max_size=0) -> None:
        self.events: Queue[EventMessage] = Queue(max_size)
        self.notices: Queue[NoticeMessage] = Queue(max_size)
        self.eose_notices: Queue[EndOfStoredEventsMessage] = Queue(max_size)
        self._unique_events: set = set()
        self.max_size = max_size
        self.lock: Lock = Lock()
    
    def add_message(self, message: str, url: str,filters:Filters):
        self._process_message(message, url,filters)

    def get_event(self):
        return self.events.get()

    def get_notice(self):
        return self.notices.get()

    def get_eose_notice(self):
        return self.eose_notices.get()

    def has_events(self):
        return self.events.qsize() > 0

    def has_notices(self):
        return self.notices.qsize() > 0

    def has_eose_notices(self):
        return self.eose_notices.qsize() > 0

    def _process_message(self, message: str, url: str,filters:Filters=None):
        message_json = json.loads(message)
        message_type = message_json[0]
        # print(message_json)
        # print(message_type)
   
        if message_type == RelayMessageType.EVENT:
            subscription_id = message_json[1]
            e = message_json[2]
            event = Event(
                e["content"],
                e["pubkey"],
                e["created_at"],
                e["kind"],
                e["tags"],
                e["sig"],
            )


            with self.lock:
                if not event.id in self._unique_events :
                    if filters is not None  and filters.match(event):
                        self.events.put(EventMessage(event, subscription_id, url))
                        self._unique_events.add(event.id)
                        if 0 < self.max_size < len(self._unique_events):
                            self._unique_events.clear()
        elif message_type == RelayMessageType.NOTICE:
            self.notices.put(NoticeMessage(message_json[1], url))
        elif message_type == RelayMessageType.END_OF_STORED_EVENTS:
            self.eose_notices.put(EndOfStoredEventsMessage(message_json[1], url))



from dataclasses import dataclass, field
from typing import Dict
import uuid

from .config import Config
from .filter import Filter, Filters
import time
from .key import PrivateKey
from .relay_manager import RelayManager
import ssl
from .message_type import ClientMessageType
import json
from .event import EventKind, EncryptedDirectMessage


@dataclass
class Agent:
    agent_id: str = str(uuid.uuid4())
    agent_name: str = None
    agent_author: str = None
    agent_desc: str = ""
    create_time: int = None
    extra_attributes: Dict[str, str] = field(default_factory=dict)
    private_key: PrivateKey = None
    url: str = None
    filters: Filters = Filters([])
    relay_manager: RelayManager = None
    max_size:int =100

    def __post_init__(self):
        filter: Filter = Filter(kinds=Config.support_kinds())
        if self.agent_name is None:
            self.agent_name = "agent_" + self.agent_id
        if self.create_time is None:
            self.create_time = int(time.time())
        if self.private_key is None:
            self.private_key = PrivateKey()
        filter.add_arbitrary_tag('p', self.private_key.public_key.hex())
            # self.filters.append(self.filter)
        if self.url is None:
            self.url = ""
        if self.relay_manager is None:
            self.relay_manager = RelayManager(self.max_size)
        self.filters.append(filter)
        self.relay_manager.add_relay(self.url,filters=self.filters)
        subscription_id = self.agent_id
        
        self.relay_manager.add_subscription_on_all_relays(subscription_id, self.filters)

        time.sleep(1.25)  # allow the connections to open



    def disconnect(self):
        self.relay_manager.close_all_relay_connections()

    def send_message(self, to: str, message: str):
        dm = EncryptedDirectMessage(
            recipient_pubkey=to,
            cleartext_content=message
        )
        self.private_key.sign_event(dm)
        self.relay_manager.publish_event(dm)

    def has_message(self):
        return self.relay_manager.message_pool.has_events()

    def get_message(self) -> Dict[str, str]:
        event_message = self.relay_manager.message_pool.get_event()
        tags = event_message.event.tags
        content = event_message.event.content
        sender = event_message.event.public_key
        if event_message.event.kind == EventKind.ENCRYPTED_DIRECT_MESSAGE:
            for e_tag in tags:
                if e_tag[0] == "p":
                    try:
                        message = self.private_key.decrypt_message(content, sender)
                        return {"sender": sender, "message": message}
                    except Exception as ex:
                        print("xxx"+str(ex)+":"+str(event_message.event))
        return None

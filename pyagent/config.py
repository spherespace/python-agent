
from .event import EventKind

class Config:

    support_kind = [EventKind.ENCRYPTED_DIRECT_MESSAGE]

    @classmethod
    def support_kinds(cls):
       return cls.support_kind


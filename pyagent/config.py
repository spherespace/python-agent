
from .event import EventKind

class Config:

    support_kinds = [EventKind.ENCRYPTED_DIRECT_MESSAGE]

    @classmethod
    def support_kinds(cls):
       return cls.support_kinds


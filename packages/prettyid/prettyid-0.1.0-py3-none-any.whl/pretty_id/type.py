from __future__ import annotations

from pretty_id.encoding import p32decode, p32encode

from uuid import UUID
from uuid_utils import uuid7


class PrettyId:
    def __init__(self, fid: str):
        self.type, id = fid.rsplit("_", 1)
        if len(id) != 26:
            raise ValueError("bad length")

        self.id = id.lower()

    @classmethod
    def random(cls, type: str) -> PrettyId:
        return cls.from_bytes(id=uuid7().bytes, type=type)

    @classmethod
    def from_bytes(cls, id: bytes, type: str) -> PrettyId:
        id_str = p32encode(id)
        obj = cls.__new__(cls)
        obj.type = type
        obj.id = id_str
        return obj

    @property
    def bytes(self):
        return p32decode(self.id)

    @classmethod
    def from_uuid(cls, uuid, type: str) -> PrettyId:
        if not hasattr(uuid, "bytes"):
            uuid = UUID(uuid)
        return cls.from_bytes(id=uuid.bytes, type=type)

    @property
    def uuid(self):
        return UUID(bytes=self.bytes)

    def __str__(self):
        return f"{self.type}_{self.id}"

    def __repr__(self):
        return f'PrettyId("{str(self)}")'

    def __lt__(self, other: PrettyId) -> bool:
        return (self.type, self.id) < (other.type, other.id)

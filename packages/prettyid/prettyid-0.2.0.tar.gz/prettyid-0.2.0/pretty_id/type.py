from __future__ import annotations
from typing import TYPE_CHECKING, Any

from pretty_id.encoding import p32decode, p32encode

from uuid import UUID
from uuid_utils import uuid7

try:
    from pydantic_core import core_schema
    _pydantic_enabled = True

except ImportError:
    _pydantic_enabled = False

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
    from pydantic.json_schema import JsonSchemaValue
    from pydantic_core import core_schema


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

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: "GetCoreSchemaHandler",
    ):
        if not _pydantic_enabled:
            raise RuntimeError("Pydantic is not installed")

        from_str_schema = core_schema.chain_schema([
            core_schema.str_schema(),
            core_schema.no_info_plain_validator_function(PrettyId),
        ])

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(PrettyId),
                from_str_schema,
            ]),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: "GetJsonSchemaHandler",
    ) -> "JsonSchemaValue":
        if not _pydantic_enabled:
            raise RuntimeError("Pydantic is not installed")

        return handler(core_schema.str_schema())

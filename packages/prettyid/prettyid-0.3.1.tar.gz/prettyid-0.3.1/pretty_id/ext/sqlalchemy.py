from __future__ import annotations

from typing import TYPE_CHECKING

from pretty_id.type import PrettyId

try:
    from sqlalchemy.types import BINARY, TypeDecorator
    from sqlalchemy.engine import Dialect
except ImportError:
    raise RuntimeError("SQLAlchemy is not installed")

if TYPE_CHECKING:
    from sqlalchemy.types import BINARY, TypeDecorator
    from sqlalchemy.engine import Dialect


class PrettyIdBinaryType(TypeDecorator[PrettyId]):
    impl = BINARY(16)
    cache_ok = True

    @property
    def python_type(self) -> type[PrettyId]:
        return PrettyId

    def __init__(self, type: str) -> None:
        self._type = type

    def process_bind_param(
        self,
        value: str | PrettyId | None,
        dialect: Dialect,
    ) -> bytes | None:
        if value is None:
            return None

        if not isinstance(value, PrettyId):
            try:
                value = PrettyId(value)
            except (TypeError, ValueError):
                return None

        if value.type != self._type:
            return None

        return value.bytes

    def process_result_value(
        self,
        value: bytes | None,
        dialect: Dialect,
    ) -> PrettyId | None:
        if value is None:
            return None
        try:
            return PrettyId.from_bytes(id=value, type=self._type)
        except Exception:
            return None

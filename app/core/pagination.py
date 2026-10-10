"""
Pagination primitives shared by every list endpoint.

A single generic envelope keeps the list contract identical across the ~530
converted doctypes, so a frontend can write one table component.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")

#: ERPNext's standard page size; kept so migrated data reads the same.
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


@dataclass
class ResultPage(Generic[T]):
    """
    Service-layer page of results -- a plain container, NOT a Pydantic model.

    This distinction matters: services hand back ORM rows, and a Pydantic model
    would try to *validate* those rows as instances of its type parameter and
    fail with PydanticSchemaGenerationError. Validation happens once, at the
    API edge, where rows are converted to Read schemas.
    """

    items: list[T]
    total: int
    offset: int
    limit: int

    @property
    def has_more(self) -> bool:
        return (self.offset + len(self.items)) < self.total

    @classmethod
    def build(
        cls, items: Sequence[T], *, total: int, offset: int, limit: int
    ) -> "ResultPage[T]":
        return cls(items=list(items), total=total, offset=offset, limit=limit)


class Page(BaseModel, Generic[T]):
    """
    API-layer envelope returned by every ``GET /`` collection endpoint.

    ``T`` is always a Read schema here, never an ORM model.
    """

    items: list[T]
    total: int = Field(description="Total rows matching the filters, ignoring paging")
    offset: int
    limit: int
    has_more: bool

    @classmethod
    def from_result(cls, result: ResultPage, items: Sequence[T]) -> "Page[T]":
        """Adopt a service ResultPage's paging metadata with validated items."""
        return cls(
            items=list(items),
            total=result.total,
            offset=result.offset,
            limit=result.limit,
            has_more=result.has_more,
        )

    @classmethod
    def build(cls, items: Sequence[T], total: int, offset: int, limit: int) -> "Page[T]":
        return cls(
            items=list(items),
            total=total,
            offset=offset,
            limit=limit,
            has_more=(offset + len(items)) < total,
        )


def normalise_paging(offset: int, limit: int) -> tuple[int, int]:
    """
    Clamp paging inputs to a safe window.

    Negative offsets and zero/negative limits are treated as the defaults
    rather than rejected, because a bad ``limit`` is a client display bug, not
    an attack -- but an unbounded ``limit`` is a DoS vector, hence MAX_PAGE_SIZE.
    """
    offset = max(0, offset)
    if limit <= 0:
        limit = DEFAULT_PAGE_SIZE
    return offset, min(limit, MAX_PAGE_SIZE)
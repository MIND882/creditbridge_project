"""
Support for ERPNext's two remaining structural concepts: **docstatus** and
**child tables**.

``docstatus``
    A submittable doctype moves Draft(0) -> Submitted(1) -> Cancelled(2). The
    transitions are guarded -- a submitted document is frozen, and a cancelled
    one is a tombstone that is excluded from every "does it exist" query. That
    exclusion is why upstream filters read ``docstatus != 2`` everywhere; here
    it is a mixin plus a repository helper so the filter cannot be forgotten.

``istable`` (child tables)
    A Frappe child table has no independent identity: it belongs to a parent,
    carries an ``idx`` for row order, and is never addressed by its own API.
    ``ChildTableModel`` supplies ``parent_id`` + ``idx``; the parent owns the
    cascade delete.
"""

from __future__ import annotations

import enum
import uuid
from typing import Optional

from sqlalchemy import Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.errors import DomainValidationError

__all__ = [
    "DocStatus",
    "SubmittableModel",
    "ChildTableModel",
    "assert_can_submit",
    "assert_can_cancel",
    "assert_can_amend",
]


class DocStatus(int, enum.Enum):
    """ERPNext's document lifecycle. Int-valued to match stored 0/1/2."""

    DRAFT = 0
    SUBMITTED = 1
    CANCELLED = 2


class SubmittableModel:
    """
    Mixin adding ``docstatus`` and the amend link.

    ``amended_from`` records which cancelled document this one replaces, so an
    amendment chain stays traceable -- the ERPNext ``amended_from`` Link field.
    """

    #: Stored as a plain Integer, matching ERPNext's 0/1/2 column. An
    #: SAEnum(DocStatus) here would persist member *names* ("DRAFT"), which
    #: silently breaks every `docstatus == 1` comparison -- those queries match
    #: nothing instead of erroring. The enum stays on the Python side for
    #: readability; the column holds the int.
    docstatus: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=DocStatus.DRAFT.value,
    )
    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, nullable=True)

    @property
    def is_draft(self) -> bool:
        return int(self.docstatus) == DocStatus.DRAFT.value  # type: ignore[arg-type]

    @property
    def is_submitted(self) -> bool:
        return int(self.docstatus) == DocStatus.SUBMITTED.value  # type: ignore[arg-type]

    @property
    def is_cancelled(self) -> bool:
        return int(self.docstatus) == DocStatus.CANCELLED.value  # type: ignore[arg-type]


class ChildTableModel:
    """
    Mixin for a Frappe ``istable`` doctype.

    ``parent_id`` is declared without a concrete FK because the parent table
    differs per child type; each child model re-declares it with its own
    ``ForeignKey`` so the constraint is real.
    """

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, nullable=True, index=True)

    #: Frappe's 1-based row order. Kept 1-based so imported rows keep their
    #: position without an off-by-one shift.
    idx: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


def assert_can_submit(doc: SubmittableModel, label: str) -> None:
    """
    Guard the 0 -> 1 transition.

    Upstream raises ``frappe.exceptions.ValidationError`` when a submitted
    document is submitted again; the same outcome, with a stable code.
    """
    if not doc.is_draft:
        raise DomainValidationError(
            f"{label} is already {'cancelled' if doc.is_cancelled else 'submitted'}",
            code="docstatus_not_draft",
        )


def assert_can_cancel(doc: SubmittableModel, label: str) -> None:
    """Guard the 1 -> 2 transition: only a submitted document can be cancelled."""
    if not doc.is_submitted:
        raise DomainValidationError(
            f"{label} must be submitted before it can be cancelled",
            code="docstatus_not_submitted",
        )


def assert_can_amend(doc: SubmittableModel, label: str) -> None:
    """Guard the 2 -> new-draft transition: only a cancelled document is amendable."""
    if not doc.is_cancelled:
        raise DomainValidationError(
            f"{label} must be cancelled before it can be amended",
            code="docstatus_not_cancelled",
        )
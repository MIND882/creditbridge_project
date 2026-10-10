"""
Shared declarative building blocks for the converted ERPNext domains.

Two deliberate departures from the surrounding CreditBridge models:

``sqlalchemy.Uuid`` instead of ``sqlalchemy.dialects.postgresql.UUID``
    The postgresql dialect type cannot be created on SQLite, which makes any
    model using it untestable without a live Postgres. ``sa.Uuid`` renders
    native ``UUID`` on Postgres (verified: the emitted DDL is ``id UUID NOT
    NULL``) and falls back to ``CHAR(32)`` elsewhere, so the same model runs
    under pytest on SQLite and in production on Postgres.

``business_id`` on the model itself
    Tenancy is a column, not a join. Every repository filters on it, which is
    what makes cross-tenant leakage a query-shape bug rather than a logic bug.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

__all__ = ["Base", "TenantModel", "new_uuid"]


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()


class TenantModel(Base):
    """
    Abstract base giving every converted doctype the same identity, tenancy and
    audit columns.

    ``abstract = True`` so no table is created for the mixin itself.
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=new_uuid)

    #: Tenant discriminator. NEVER settable from a request body -- it is always
    #: injected by the service from the authenticated context.
    #:
    #: The FK matches the existing domain models in this repo (lead,
    #: opportunity): deleting a business cascades to everything it owns, so a
    #: converted doctype can never outlive its tenant as an orphan.
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<{type(self).__name__} id={self.id} business_id={self.business_id}>"


def tenant_index(name: str, *columns: str) -> Index:
    """
    Convenience builder for the near-universal ``(business_id, <cols>)` index.

    Tenancy comes first because it is the leading column of every filtered
    query; putting it first keeps the index usable for the tenant-only prefix.
    """
    return Index(name, "business_id", *columns)


def as_dict(obj: Any) -> dict[str, Any]:  # pragma: no cover - convenience
    return {c.key: getattr(obj, c.key) for c in obj.__table__.columns}
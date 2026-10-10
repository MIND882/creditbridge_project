"""

Bisect Nodes -- converted from ``erpnext/accounts/doctype/bisect_nodes``.





"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, DateTime, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["BisectNodes"]







class BisectNodes(TenantModel):

    __tablename__ = "bisect_nodes"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bisect_nodes_business_name"),

    )



    #: ``autoname`` = 'autoincrement'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    root: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    left_child: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    right_child: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    period_from_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    period_to_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    difference: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    balance_sheet_summary: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    profit_loss_summary: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    generated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BisectNodes id={self.id}>"

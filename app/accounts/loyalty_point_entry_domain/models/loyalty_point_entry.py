"""

Loyalty Point Entry -- converted from ``erpnext/accounts/doctype/loyalty_point_entry``.





"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Integer, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["LoyaltyPointEntry"]







class LoyaltyPointEntry(TenantModel):

    __tablename__ = "loyalty_point_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_loyalty_point_entries_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    loyalty_program: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    loyalty_program_tier: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    redeem_against: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    loyalty_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    purchase_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    expiry_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    invoice_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    discretionary_reason: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LoyaltyPointEntry id={self.id}>"

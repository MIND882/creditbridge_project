"""

Ledger Health -- converted from ``erpnext/accounts/doctype/ledger_health``.





"""



from __future__ import annotations



import datetime as dt

from typing import Optional

import uuid



from sqlalchemy import Boolean, DateTime, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel



__all__ = ["LedgerHealth"]







class LedgerHealth(TenantModel):

    __tablename__ = "ledger_healths"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_ledger_healths_business_name"),

    )



    #: ``autoname`` = 'autoincrement'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    debit_credit_mismatch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    checked_on: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    general_and_payment_ledger_mismatch: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LedgerHealth id={self.id}>"

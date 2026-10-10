"""

Advance Payment Ledger Entry -- converted from ``erpnext/accounts/doctype/advance_payment_ledger_entry``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["AdvancePaymentLedgerEntry"]







class AdvancePaymentLedgerEntry(SubmittableModel, TenantModel):

    __tablename__ = "advance_payment_ledger_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_advance_payment_ledger_entries_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    against_voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    against_voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    event: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delinked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    base_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AdvancePaymentLedgerEntry id={self.id}>"

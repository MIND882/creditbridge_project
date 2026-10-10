"""

Repost Payment Ledger -- converted from ``erpnext/accounts/doctype/repost_payment_ledger``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.repost_payment_ledger_items_domain.models.repost_payment_ledger_items import RepostPaymentLedgerItems



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["RepostPaymentLedger", "RepostPaymentLedgerRepostStatus"]







class RepostPaymentLedgerRepostStatus(str, enum.Enum):

    QUEUED = "Queued"

    FAILED = "Failed"

    COMPLETED = "Completed"









class RepostPaymentLedger(SubmittableModel, TenantModel):

    __tablename__ = "repost_payment_ledgers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_repost_payment_ledgers_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    repost_status: Mapped[Optional[RepostPaymentLedgerRepostStatus]] = mapped_column(

        SAEnum(RepostPaymentLedgerRepostStatus, native_enum=False, length=9, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    add_manually: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    repost_error_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    repost_vouchers = relationship(

        RepostPaymentLedgerItems,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=RepostPaymentLedgerItems.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<RepostPaymentLedger id={self.id}>"

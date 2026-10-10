"""

Repost Accounting Ledger -- converted from ``erpnext/accounts/doctype/repost_accounting_ledger``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.repost_accounting_ledger_items_domain.models.repost_accounting_ledger_items import RepostAccountingLedgerItems



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["RepostAccountingLedger", "RepostAccountingLedgerStatus"]







class RepostAccountingLedgerStatus(str, enum.Enum):

    QUEUED = "Queued"

    IN_PROGRESS = "In Progress"

    PARTIALLY_REPOSTED = "Partially Reposted"

    COMPLETED = "Completed"

    FAILED = "Failed"

    CANCELLED = "Cancelled"









class RepostAccountingLedger(SubmittableModel, TenantModel):

    __tablename__ = "repost_accounting_ledgers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_repost_accounting_ledgers_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    delete_cancelled_entries: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    error_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[Optional[RepostAccountingLedgerStatus]] = mapped_column(

        SAEnum(RepostAccountingLedgerStatus, native_enum=False, length=18, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    scheduled_job: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    vouchers = relationship(

        RepostAccountingLedgerItems,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=RepostAccountingLedgerItems.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<RepostAccountingLedger id={self.id}>"

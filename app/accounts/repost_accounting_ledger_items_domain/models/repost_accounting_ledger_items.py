"""

Repost Accounting Ledger Items -- converted from ``erpnext/accounts/doctype/repost_accounting_ledger_items``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, ForeignKey, String, Text, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["RepostAccountingLedgerItems", "RepostAccountingLedgerItemsStatus"]







class RepostAccountingLedgerItemsStatus(str, enum.Enum):

    PENDING = "Pending"

    REPOSTED = "Reposted"

    SKIPPED = "Skipped"

    FAILED = "Failed"









class RepostAccountingLedgerItems(ChildTableModel, TenantModel):

    __tablename__ = "repost_accounting_ledger_items"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("repost_accounting_ledgers.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("RepostAccountingLedger", back_populates="vouchers", foreign_keys=[parent_id])



    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[Optional[RepostAccountingLedgerItemsStatus]] = mapped_column(

        SAEnum(RepostAccountingLedgerItemsStatus, native_enum=False, length=8, validate_strings=True),

        nullable=True,

    )

    traceback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<RepostAccountingLedgerItems id={self.id}>"

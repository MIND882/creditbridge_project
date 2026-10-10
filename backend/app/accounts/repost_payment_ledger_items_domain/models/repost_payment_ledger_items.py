"""

Repost Payment Ledger Items -- converted from ``erpnext/accounts/doctype/repost_payment_ledger_items``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["RepostPaymentLedgerItems"]







class RepostPaymentLedgerItems(ChildTableModel, TenantModel):

    __tablename__ = "repost_payment_ledger_items"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("repost_payment_ledgers.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("RepostPaymentLedger", back_populates="repost_vouchers", foreign_keys=[parent_id])



    voucher_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    voucher_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<RepostPaymentLedgerItems id={self.id}>"

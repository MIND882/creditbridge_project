"""

Unreconcile Payment Entries -- converted from ``erpnext/accounts/doctype/unreconcile_payment_entries``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["UnreconcilePaymentEntries"]







class UnreconcilePaymentEntries(ChildTableModel, TenantModel):

    __tablename__ = "unreconcile_payment_entries"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("unreconcile_payments.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("UnreconcilePayment", back_populates="allocations", foreign_keys=[parent_id])



    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    allocated_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    unlinked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    reference_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    account: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<UnreconcilePaymentEntries id={self.id}>"

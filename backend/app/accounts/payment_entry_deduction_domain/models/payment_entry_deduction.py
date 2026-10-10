"""

PaymentEntryDeduction -- converted from ``erpnext/accounts/doctype/payment_entry_deduction``.



Rows only ever exist inside a parent, so the API is read-only.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, Numeric, Text, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PaymentEntryDeduction"]





class PaymentEntryDeduction(ChildTableModel, TenantModel):

    """One row of ``PaymentEntry.deductions``."""



    __tablename__ = "payment_entry_deductions"



    parent_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("payment_entries.id", ondelete="CASCADE"), nullable=False, index=True

    )

    parent = relationship("PaymentEntry", back_populates="deductions", foreign_keys=[parent_id])



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=False, index=True

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_exchange_gain_loss: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentEntryDeduction id={self.id}>"

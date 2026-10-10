"""

Cashier Closing Payments -- converted from ``erpnext/accounts/doctype/cashier_closing_payments``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPayment  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["CashierClosingPayments"]







class CashierClosingPayments(ChildTableModel, TenantModel):

    __tablename__ = "cashier_closing_payments"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cashier_closings.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("CashierClosing", back_populates="payments", foreign_keys=[parent_id])



    mode_of_payment_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("mode_of_payments.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    mode_of_payment = relationship("ModeOfPayment", foreign_keys=[mode_of_payment_id])

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<CashierClosingPayments id={self.id}>"

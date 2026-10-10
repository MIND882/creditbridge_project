"""

Payment Reconciliation Payment -- converted from ``erpnext/accounts/doctype/payment_reconciliation_payment``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PaymentReconciliationPayment"]







class PaymentReconciliationPayment(ChildTableModel, TenantModel):

    __tablename__ = "payment_reconciliation_payments"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_reconciliations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PaymentReconciliation", back_populates="payments", foreign_keys=[parent_id])



    reference_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    is_advance: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_row: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    difference_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    remarks: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentReconciliationPayment id={self.id}>"

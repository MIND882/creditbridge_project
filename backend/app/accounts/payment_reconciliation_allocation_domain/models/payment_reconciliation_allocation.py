"""

Payment Reconciliation Allocation -- converted from ``erpnext/accounts/doctype/payment_reconciliation_allocation``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PaymentReconciliationAllocation"]







class PaymentReconciliationAllocation(ChildTableModel, TenantModel):

    __tablename__ = "payment_reconciliation_allocations"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_reconciliations.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("PaymentReconciliation", back_populates="allocation", foreign_keys=[parent_id])



    invoice_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    difference_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    difference_account = relationship("Account", foreign_keys=[difference_account_id])

    difference_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_advance: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    invoice_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    unreconciled_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reference_row: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    gain_loss_posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    debit_or_credit_note_posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PaymentReconciliationAllocation id={self.id}>"

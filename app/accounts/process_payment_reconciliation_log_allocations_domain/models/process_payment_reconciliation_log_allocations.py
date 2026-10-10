"""

Process Payment Reconciliation Log Allocations -- converted from ``erpnext/accounts/doctype/process_payment_reconciliation_log_allocations``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ProcessPaymentReconciliationLogAllocations"]







class ProcessPaymentReconciliationLogAllocations(ChildTableModel, TenantModel):

    __tablename__ = "process_payment_reconciliation_log_allocations"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("process_payment_reconciliation_logs.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("ProcessPaymentReconciliationLog", back_populates="allocations", foreign_keys=[parent_id])



    reference_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_row: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    invoice_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    invoice_number: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    unreconciled_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    is_advance: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    difference_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    difference_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    difference_account = relationship("Account", foreign_keys=[difference_account_id])

    exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reconciled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    gain_loss_posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProcessPaymentReconciliationLogAllocations id={self.id}>"

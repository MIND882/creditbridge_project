"""

Process Payment Reconciliation -- converted from ``erpnext/accounts/doctype/process_payment_reconciliation``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.cost_center_domain.models.cost_center import CostCenter  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["ProcessPaymentReconciliation", "ProcessPaymentReconciliationStatus"]







class ProcessPaymentReconciliationStatus(str, enum.Enum):

    QUEUED = "Queued"

    RUNNING = "Running"

    PAUSED = "Paused"

    COMPLETED = "Completed"

    PARTIALLY_RECONCILED = "Partially Reconciled"

    FAILED = "Failed"

    CANCELLED = "Cancelled"









class ProcessPaymentReconciliation(SubmittableModel, TenantModel):

    __tablename__ = "process_payment_reconciliations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_process_payment_reconciliations_business_name"),

    )



    #: ``autoname`` = 'format:ACC-PPR-{#####}'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    status: Mapped[Optional[ProcessPaymentReconciliationStatus]] = mapped_column(

        SAEnum(ProcessPaymentReconciliationStatus, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    receivable_payable_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    receivable_payable_account = relationship("Account", foreign_keys=[receivable_payable_account_id])

    from_invoice_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_invoice_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    from_payment_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_payment_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    bank_cash_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bank_cash_account = relationship("Account", foreign_keys=[bank_cash_account_id])

    error_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    default_advance_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_advance_account = relationship("Account", foreign_keys=[default_advance_account_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProcessPaymentReconciliation id={self.id}>"

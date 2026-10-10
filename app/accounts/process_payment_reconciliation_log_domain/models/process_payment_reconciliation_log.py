"""

Process Payment Reconciliation Log -- converted from ``erpnext/accounts/doctype/process_payment_reconciliation_log``.





"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, Integer, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.process_payment_reconciliation_log_allocations_domain.models.process_payment_reconciliation_log_allocations import ProcessPaymentReconciliationLogAllocations



from app.core.base_model import TenantModel



__all__ = ["ProcessPaymentReconciliationLog", "ProcessPaymentReconciliationLogStatus"]







class ProcessPaymentReconciliationLogStatus(str, enum.Enum):

    RUNNING = "Running"

    PAUSED = "Paused"

    RECONCILED = "Reconciled"

    PARTIALLY_RECONCILED = "Partially Reconciled"

    FAILED = "Failed"

    CANCELLED = "Cancelled"









class ProcessPaymentReconciliationLog(TenantModel):

    __tablename__ = "process_payment_reconciliation_logs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_process_payment_reconciliation_logs_business_name"),

    )



    #: ``autoname`` = 'format:PPR-LOG-{##}'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    reconciled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    total_allocations: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    allocated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    reconciled_entries: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    error_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    process_pr: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    status: Mapped[Optional[ProcessPaymentReconciliationLogStatus]] = mapped_column(

        SAEnum(ProcessPaymentReconciliationLogStatus, native_enum=False, length=20, validate_strings=True),

        nullable=True,

    )



    allocations = relationship(

        ProcessPaymentReconciliationLogAllocations,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=ProcessPaymentReconciliationLogAllocations.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProcessPaymentReconciliationLog id={self.id}>"

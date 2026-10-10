"""

Process Deferred Accounting -- converted from ``erpnext/accounts/doctype/process_deferred_accounting``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["ProcessDeferredAccounting", "ProcessDeferredAccountingType"]







class ProcessDeferredAccountingType(str, enum.Enum):

    INCOME = "Income"

    EXPENSE = "Expense"









class ProcessDeferredAccounting(SubmittableModel, TenantModel):

    __tablename__ = "process_deferred_accountings"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_process_deferred_accountings_business_name"),

    )



    #: ``autoname`` = 'ACC-PDA-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    type: Mapped[ProcessDeferredAccountingType] = mapped_column(

        SAEnum(ProcessDeferredAccountingType, native_enum=False, length=7, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    start_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    end_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProcessDeferredAccounting id={self.id}>"

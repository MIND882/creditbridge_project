"""

Period Closing Voucher -- converted from ``erpnext/accounts/doctype/period_closing_voucher``.



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

from app.accounts.fiscal_year_domain.models.fiscal_year import FiscalYear  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["PeriodClosingVoucher", "PeriodClosingVoucherGleProcessingStatus"]







class PeriodClosingVoucherGleProcessingStatus(str, enum.Enum):

    IN_PROGRESS = "In Progress"

    COMPLETED = "Completed"

    FAILED = "Failed"









class PeriodClosingVoucher(SubmittableModel, TenantModel):

    __tablename__ = "period_closing_vouchers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_period_closing_vouchers_business_name"),

    )



    #: ``autoname`` = 'ACC-PCV-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    transaction_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    fiscal_year_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("fiscal_years.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    fiscal_year = relationship("FiscalYear", foreign_keys=[fiscal_year_id])

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    closing_account_head_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    closing_account_head = relationship("Account", foreign_keys=[closing_account_head_id])

    remarks: Mapped[str] = mapped_column(String(140), nullable=False)

    gle_processing_status: Mapped[Optional[PeriodClosingVoucherGleProcessingStatus]] = mapped_column(

        SAEnum(PeriodClosingVoucherGleProcessingStatus, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    period_end_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    period_start_date: Mapped[dt.date] = mapped_column(Date, nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PeriodClosingVoucher id={self.id}>"

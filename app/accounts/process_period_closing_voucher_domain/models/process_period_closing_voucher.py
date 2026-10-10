"""

Process Period Closing Voucher -- converted from ``erpnext/accounts/doctype/process_period_closing_voucher``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.process_period_closing_voucher_detail_domain.models.process_period_closing_voucher_detail import ProcessPeriodClosingVoucherDetail



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["ProcessPeriodClosingVoucher", "ProcessPeriodClosingVoucherStatus"]







class ProcessPeriodClosingVoucherStatus(str, enum.Enum):

    QUEUED = "Queued"

    RUNNING = "Running"

    PAUSED = "Paused"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"









class ProcessPeriodClosingVoucher(SubmittableModel, TenantModel):

    __tablename__ = "process_period_closing_vouchers"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_process_period_closing_vouchers_business_name"),

    )



    #: ``autoname`` = 'format:Process-PCV-{###}'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    parent_pcv: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    status: Mapped[Optional[ProcessPeriodClosingVoucherStatus]] = mapped_column(

        SAEnum(ProcessPeriodClosingVoucherStatus, native_enum=False, length=9, validate_strings=True),

        nullable=True,

    )

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    p_l_closing_balance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    bs_closing_balance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)



    normal_balances = relationship(

        ProcessPeriodClosingVoucherDetail,

        primaryjoin="and_(ProcessPeriodClosingVoucher.id == foreign(ProcessPeriodClosingVoucherDetail.parent_id), ProcessPeriodClosingVoucherDetail.parenttype == 'Process Period Closing Voucher')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=ProcessPeriodClosingVoucherDetail.idx,

        overlaps="z_opening_balances",

    )

    z_opening_balances = relationship(

        ProcessPeriodClosingVoucherDetail,

        primaryjoin="and_(ProcessPeriodClosingVoucher.id == foreign(ProcessPeriodClosingVoucherDetail.parent_id), ProcessPeriodClosingVoucherDetail.parenttype == 'Process Period Closing Voucher')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=ProcessPeriodClosingVoucherDetail.idx,

        overlaps="normal_balances",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProcessPeriodClosingVoucher id={self.id}>"

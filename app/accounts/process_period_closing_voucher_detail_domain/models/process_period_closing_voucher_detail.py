"""

Process Period Closing Voucher Detail -- converted from ``erpnext/accounts/doctype/process_period_closing_voucher_detail``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, String, Text, Uuid

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ProcessPeriodClosingVoucherDetail", "ProcessPeriodClosingVoucherDetailStatus", "ProcessPeriodClosingVoucherDetailReportType"]







class ProcessPeriodClosingVoucherDetailStatus(str, enum.Enum):

    QUEUED = "Queued"

    RUNNING = "Running"

    PAUSED = "Paused"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"





class ProcessPeriodClosingVoucherDetailReportType(str, enum.Enum):

    PROFIT_AND_LOSS = "Profit and Loss"

    BALANCE_SHEET = "Balance Sheet"









class ProcessPeriodClosingVoucherDetail(ChildTableModel, TenantModel):

    __tablename__ = "process_period_closing_voucher_details"

    #: Polymorphic parent -- process_period_closing_voucher, process_period_closing_voucher

    #: all use this doctype as a Table, so there is no single

    #: foreign key to point at. ``parenttype`` says which.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        Uuid, nullable=True, index=True

    )

    parenttype: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True, index=True

    )



    processing_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    status: Mapped[Optional[ProcessPeriodClosingVoucherDetailStatus]] = mapped_column(

        SAEnum(ProcessPeriodClosingVoucherDetailStatus, native_enum=False, length=9, validate_strings=True),

        nullable=True,

    )

    closing_balance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    report_type: Mapped[Optional[ProcessPeriodClosingVoucherDetailReportType]] = mapped_column(

        SAEnum(ProcessPeriodClosingVoucherDetailReportType, native_enum=False, length=15, validate_strings=True),

        nullable=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProcessPeriodClosingVoucherDetail id={self.id}>"

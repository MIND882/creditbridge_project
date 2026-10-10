"""

POS Invoice Merge Log -- converted from ``erpnext/accounts/doctype/pos_invoice_merge_log``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, String, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.pos_invoice_reference_domain.models.pos_invoice_reference import POSInvoiceReference



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["POSInvoiceMergeLog", "POSInvoiceMergeLogMergeInvoicesBasedOn"]







class POSInvoiceMergeLogMergeInvoicesBasedOn(str, enum.Enum):

    CUSTOMER = "Customer"

    CUSTOMER_GROUP = "Customer Group"









class POSInvoiceMergeLog(SubmittableModel, TenantModel):

    __tablename__ = "pos_invoice_merge_logs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pos_invoice_merge_logs_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    consolidated_invoice: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    consolidated_credit_note: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pos_closing_entry: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    merge_invoices_based_on: Mapped[POSInvoiceMergeLogMergeInvoicesBasedOn] = mapped_column(

        SAEnum(POSInvoiceMergeLogMergeInvoicesBasedOn, native_enum=False, length=14, validate_strings=True),

        nullable=False,

    )

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)



    pos_invoices = relationship(

        POSInvoiceReference,

        primaryjoin="and_(POSInvoiceMergeLog.id == foreign(POSInvoiceReference.parent_id), POSInvoiceReference.parenttype == 'POS Invoice Merge Log')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=POSInvoiceReference.idx,

        overlaps="pos_invoices",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSInvoiceMergeLog id={self.id}>"

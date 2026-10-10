"""

POS Closing Entry -- converted from ``erpnext/accounts/doctype/pos_closing_entry``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, DateTime, Enum as SAEnum, Numeric, String, Time, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.pos_closing_entry_detail_domain.models.pos_closing_entry_detail import POSClosingEntryDetail

from app.accounts.pos_closing_entry_taxes_domain.models.pos_closing_entry_taxes import POSClosingEntryTaxes

from app.accounts.pos_invoice_reference_domain.models.pos_invoice_reference import POSInvoiceReference

from app.accounts.sales_invoice_reference_domain.models.sales_invoice_reference import SalesInvoiceReference



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["POSClosingEntry", "POSClosingEntryStatus"]







class POSClosingEntryStatus(str, enum.Enum):

    DRAFT = "Draft"

    SUBMITTED = "Submitted"

    QUEUED = "Queued"

    FAILED = "Failed"

    CANCELLED = "Cancelled"









class POSClosingEntry(SubmittableModel, TenantModel):

    __tablename__ = "pos_closing_entries"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pos_closing_entries_business_name"),

    )



    #: ``autoname`` = 'POS-CLO-.YYYY.-.#####'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    period_start_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    period_end_date: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    pos_profile: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    user: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    net_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amended_from: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    pos_opening_entry: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    status: Mapped[Optional[POSClosingEntryStatus]] = mapped_column(

        SAEnum(POSClosingEntryStatus, native_enum=False, length=9, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    error_message: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    posting_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    total_taxes_and_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    payment_reconciliation = relationship(

        POSClosingEntryDetail,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSClosingEntryDetail.idx,

        passive_deletes=True,

    )

    taxes = relationship(

        POSClosingEntryTaxes,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=POSClosingEntryTaxes.idx,

        passive_deletes=True,

    )

    pos_invoices = relationship(

        POSInvoiceReference,

        primaryjoin="and_(POSClosingEntry.id == foreign(POSInvoiceReference.parent_id), POSInvoiceReference.parenttype == 'POS Closing Entry')",

        cascade="all, delete-orphan",

        single_parent=True,

        order_by=POSInvoiceReference.idx,

        overlaps="pos_invoices",

    )

    sales_invoices = relationship(

        SalesInvoiceReference,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=SalesInvoiceReference.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSClosingEntry id={self.id}>"

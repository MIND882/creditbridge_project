"""

Proforma Invoice -- converted from ``erpnext/selling/doctype/proforma_invoice``.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, DateTime, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.selling.proforma_invoice_item_domain.models.proforma_invoice_item import ProformaInvoiceItem



from app.core.base_model import TenantModel



__all__ = ["ProformaInvoice", "ProformaInvoiceNamingSeries", "ProformaInvoiceBasedOn", "ProformaInvoiceStatus"]





class ProformaInvoiceNamingSeries(str, enum.Enum):

    PRO_YYYY = "PRO-.YYYY.-"



class ProformaInvoiceBasedOn(str, enum.Enum):

    QUANTITY = "Quantity"

    AMOUNT = "Amount"



class ProformaInvoiceStatus(str, enum.Enum):

    DRAFT = "Draft"

    ISSUED = "Issued"

    CANCELLED = "Cancelled"





class ProformaInvoice(TenantModel):

    __tablename__ = "proforma_invoices"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_proforma_invoices_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(ProformaInvoiceNamingSeries,values_callable=lambda x: [e.value for e in x],  native_enum=False, length=15, validate_strings=True), nullable=False)

    sales_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("sales_orders.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    sales_order = relationship("app.selling.sales_order_domain.models.sales_order.SalesOrder", foreign_keys=[sales_order_id])

    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_customers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    customer = relationship("app.selling.customer_domain.models.customer.Customer", foreign_keys=[customer_id])

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    proforma_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    based_on: Mapped[Optional[str]] = mapped_column(SAEnum(ProformaInvoiceBasedOn,values_callable=lambda x: [e.value for e in x],  native_enum=False, length=12, validate_strings=True), nullable=True)

    hide_item_qty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    total_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    grand_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    print_format: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    proforma_pdf: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(ProformaInvoiceStatus, values_callable=lambda x: [e.value for e in x], native_enum=False, length=13, validate_strings=True), nullable=True)

    sent_on: Mapped[Optional[dt.datetime]] = mapped_column(DateTime, nullable=True)

    emailed_to: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("proforma_invoices.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.selling.proforma_invoice_domain.models.proforma_invoice.ProformaInvoice", foreign_keys=[amended_from_id])



    items: Mapped[list["ProformaInvoiceItem"]] = relationship(  # noqa: F821

        "app.selling.proforma_invoice_item_domain.models.proforma_invoice_item.ProformaInvoiceItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys=[ProformaInvoiceItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProformaInvoice id={self.id}>"

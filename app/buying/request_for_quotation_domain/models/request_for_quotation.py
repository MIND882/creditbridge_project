"""

Request for Quotation -- converted from ``erpnext/buying/doctype/request_for_quotation``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.buying.request_for_quotation_supplier_domain.models.request_for_quotation_supplier import RequestForQuotationSupplier

from app.buying.request_for_quotation_item_domain.models.request_for_quotation_item import RequestForQuotationItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["RequestForQuotation", "RequestForQuotationNamingSeries", "RequestForQuotationStatus"]





class RequestForQuotationNamingSeries(str, enum.Enum):

    PUR_RFQ_YYYY = "PUR-RFQ-.YYYY.-"



class RequestForQuotationStatus(str, enum.Enum):

    DRAFT = "Draft"

    SUBMITTED = "Submitted"

    CANCELLED = "Cancelled"





class RequestForQuotation(SubmittableModel, TenantModel):

    __tablename__ = "request_for_quotations"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_request_for_quotations_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(RequestForQuotationNamingSeries, native_enum=False, length=19, validate_strings=True), nullable=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    vendor_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("suppliers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    vendor = relationship("app.buying.supplier_domain.models.supplier.Supplier", foreign_keys=[vendor_id])

    transaction_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    email_template: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    message_for_supplier: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    opportunity: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[str] = mapped_column(SAEnum(RequestForQuotationStatus, native_enum=False, length=13, validate_strings=True), nullable=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("request_for_quotations.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.buying.request_for_quotation_domain.models.request_for_quotation.RequestForQuotation", foreign_keys=[amended_from_id])

    schedule_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    incoterm: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    named_place: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    send_attached_files: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    send_document_print: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    billing_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    billing_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    has_unit_price_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    subject: Mapped[str] = mapped_column(String(140), nullable=False)

    mfs_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    use_html: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    shipping_address: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    shipping_address_display: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    suppliers: Mapped[list["RequestForQuotationSupplier"]] = relationship(  # noqa: F821

        "RequestForQuotationSupplier",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[RequestForQuotationSupplier.parent_id]",

    )



    items: Mapped[list["RequestForQuotationItem"]] = relationship(  # noqa: F821

        "RequestForQuotationItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[RequestForQuotationItem.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<RequestForQuotation id={self.id}>"

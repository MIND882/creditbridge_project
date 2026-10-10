"""

Quality Inspection -- converted from ``erpnext/stock/doctype/quality_inspection``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.quality_inspection_reading_domain.models.quality_inspection_reading import QualityInspectionReading



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["QualityInspection", "QualityInspectionNamingSeries", "QualityInspectionInspectionType", "QualityInspectionReferenceType", "QualityInspectionStatus"]





class QualityInspectionNamingSeries(str, enum.Enum):

    MAT_QA_YYYY = "MAT-QA-.YYYY.-"



class QualityInspectionInspectionType(str, enum.Enum):

    INCOMING = "Incoming"

    OUTGOING = "Outgoing"

    IN_PROCESS = "In Process"



class QualityInspectionReferenceType(str, enum.Enum):

    PURCHASE_RECEIPT = "Purchase Receipt"

    PURCHASE_INVOICE = "Purchase Invoice"

    SUBCONTRACTING_RECEIPT = "Subcontracting Receipt"

    DELIVERY_NOTE = "Delivery Note"

    SALES_INVOICE = "Sales Invoice"

    STOCK_ENTRY = "Stock Entry"

    JOB_CARD = "Job Card"



class QualityInspectionStatus(str, enum.Enum):

    ACCEPTED = "Accepted"

    REJECTED = "Rejected"

    CANCELLED = "Cancelled"





class QualityInspection(SubmittableModel, TenantModel):

    __tablename__ = "quality_inspections"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_quality_inspections_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(QualityInspectionNamingSeries, native_enum=False, length=18, validate_strings=True), nullable=False)

    report_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    inspection_type: Mapped[str] = mapped_column(SAEnum(QualityInspectionInspectionType, native_enum=False, length=14, validate_strings=True), nullable=False)

    reference_type: Mapped[str] = mapped_column(SAEnum(QualityInspectionReferenceType, native_enum=False, length=26, validate_strings=True), nullable=False)

    reference_name: Mapped[str] = mapped_column(String(140), nullable=False)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("Item", foreign_keys=[item_code_id])

    item_serial_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("serial_nos.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_serial_no = relationship("SerialNo", foreign_keys=[item_serial_no_id])

    batch_no_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("batchs.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    batch_no = relationship("Batch", foreign_keys=[batch_no_id])

    sample_size: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    inspected_by: Mapped[str] = mapped_column(String(140), nullable=False)

    verified_by: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    bom_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspections.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("QualityInspection", foreign_keys=[amended_from_id])

    quality_inspection_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    quality_inspection_template = relationship("QualityInspectionTemplate", foreign_keys=[quality_inspection_template_id])

    status: Mapped[str] = mapped_column(SAEnum(QualityInspectionStatus, native_enum=False, length=13, validate_strings=True), nullable=False)

    manual_inspection: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    child_row_reference: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    readings: Mapped[list["QualityInspectionReading"]] = relationship(  # noqa: F821

        "QualityInspectionReading",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[QualityInspectionReading.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<QualityInspection id={self.id}>"

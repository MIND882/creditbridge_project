"""

Material Request -- converted from ``erpnext/stock/doctype/material_request``.



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



from app.stock.material_request_item_domain.models.material_request_item import MaterialRequestItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["MaterialRequest", "MaterialRequestNamingSeries", "MaterialRequestMaterialRequestType", "MaterialRequestStatus", "MaterialRequestTransferStatus"]





class MaterialRequestNamingSeries(str, enum.Enum):

    MAT_MR_YYYY = "MAT-MR-.YYYY.-"



class MaterialRequestMaterialRequestType(str, enum.Enum):

    PURCHASE = "Purchase"

    MATERIAL_TRANSFER = "Material Transfer"

    MATERIAL_ISSUE = "Material Issue"

    MANUFACTURE = "Manufacture"

    SUBCONTRACTING = "Subcontracting"

    CUSTOMER_PROVIDED = "Customer Provided"



class MaterialRequestStatus(str, enum.Enum):

    DRAFT = "Draft"

    SUBMITTED = "Submitted"

    STOPPED = "Stopped"

    CANCELLED = "Cancelled"

    PENDING = "Pending"

    PARTIALLY_ORDERED = "Partially Ordered"

    PARTIALLY_RECEIVED = "Partially Received"

    ORDERED = "Ordered"

    ISSUED = "Issued"

    TRANSFERRED = "Transferred"

    RECEIVED = "Received"



class MaterialRequestTransferStatus(str, enum.Enum):

    NOT_STARTED = "Not Started"

    IN_TRANSIT = "In Transit"

    COMPLETED = "Completed"





class MaterialRequest(SubmittableModel, TenantModel):

    __tablename__ = "material_requests"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_material_requests_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(MaterialRequestNamingSeries, native_enum=False, length=18, validate_strings=True), nullable=False)

    title: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    material_request_type: Mapped[str] = mapped_column(SAEnum(MaterialRequestMaterialRequestType, native_enum=False, length=21, validate_strings=True), nullable=False)

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    schedule_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("MaterialRequest", foreign_keys=[amended_from_id])

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    transaction_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(MaterialRequestStatus, native_enum=False, length=22, validate_strings=True), nullable=True)

    per_ordered: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    per_received: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    select_print_heading: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    tc_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    job_card: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    set_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_warehouse = relationship("Warehouse", foreign_keys=[set_warehouse_id])

    set_from_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    set_from_warehouse = relationship("Warehouse", foreign_keys=[set_from_warehouse_id])

    transfer_status: Mapped[Optional[str]] = mapped_column(SAEnum(MaterialRequestTransferStatus, native_enum=False, length=15, validate_strings=True), nullable=True)

    work_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    buying_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    buying_price_list = relationship("PriceList", foreign_keys=[buying_price_list_id])

    last_scanned_warehouse: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    auto_created_via_reorder: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    items: Mapped[list["MaterialRequestItem"]] = relationship(  # noqa: F821

        "MaterialRequestItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[MaterialRequestItem.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<MaterialRequest id={self.id}>"

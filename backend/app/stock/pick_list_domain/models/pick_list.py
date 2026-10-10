"""

Pick List -- converted from ``erpnext/stock/doctype/pick_list``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.stock.pick_list_item_domain.models.pick_list_item import PickListItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["PickList", "PickListPurpose", "PickListNamingSeries", "PickListStatus", "PickListDeliveryStatus"]





class PickListPurpose(str, enum.Enum):

    MATERIAL_TRANSFER_FOR_MANUFACTURE = "Material Transfer for Manufacture"

    MATERIAL_TRANSFER = "Material Transfer"

    DELIVERY = "Delivery"



class PickListNamingSeries(str, enum.Enum):

    STO_PICK_YYYY = "STO-PICK-.YYYY.-"



class PickListStatus(str, enum.Enum):

    DRAFT = "Draft"

    OPEN = "Open"

    PARTLY_DELIVERED = "Partly Delivered"

    PARTIALLY_TRANSFERRED = "Partially Transferred"

    COMPLETED = "Completed"

    CANCELLED = "Cancelled"



class PickListDeliveryStatus(str, enum.Enum):

    NOT_DELIVERED = "Not Delivered"

    FULLY_DELIVERED = "Fully Delivered"

    PARTLY_DELIVERED = "Partly Delivered"





class PickList(SubmittableModel, TenantModel):

    __tablename__ = "pick_lists"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_pick_lists_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    company: Mapped[str] = mapped_column(String(140), nullable=False)

    parent_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    parent_warehouse = relationship("Warehouse", foreign_keys=[parent_warehouse_id])

    customer: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    work_order: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    for_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pick_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("PickList", foreign_keys=[amended_from_id])

    purpose: Mapped[Optional[str]] = mapped_column(SAEnum(PickListPurpose, native_enum=False, length=37, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    material_request_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("material_requests.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    material_request = relationship("MaterialRequest", foreign_keys=[material_request_id])

    naming_series: Mapped[str] = mapped_column(SAEnum(PickListNamingSeries, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    group_same_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    scan_barcode: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    scan_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    prompt_qty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    status: Mapped[str] = mapped_column(SAEnum(PickListStatus, native_enum=False, length=25, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    consider_rejected_warehouses: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    pick_manually: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    ignore_pricing_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    delivery_status: Mapped[Optional[str]] = mapped_column(SAEnum(PickListDeliveryStatus, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    per_delivered: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)



    locations: Mapped[list["PickListItem"]] = relationship(  # noqa: F821

        "PickListItem",

        back_populates="parent",

        cascade="all, delete-orphan",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        foreign_keys="[PickListItem.parent_id]",

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PickList id={self.id}>"

"""

BOM Creator -- converted from ``erpnext/manufacturing/doctype/bom_creator``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.bom_creator_item_domain.models.bom_creator_item import BomCreatorItem



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["BomCreator", "BomCreatorRmCostAsPer", "BomCreatorStatus"]





class BomCreatorRmCostAsPer(str, enum.Enum):

    VALUATION_RATE = "Valuation Rate"

    LAST_PURCHASE_RATE = "Last Purchase Rate"

    PRICE_LIST = "Price List"



class BomCreatorStatus(str, enum.Enum):

    DRAFT = "Draft"

    SUBMITTED = "Submitted"

    IN_PROGRESS = "In Progress"

    COMPLETED = "Completed"

    FAILED = "Failed"

    CANCELLED = "Cancelled"





class BomCreator(SubmittableModel, TenantModel):

    __tablename__ = "bom_creators"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bom_creators_business_name"),

    )



    #: ``autoname`` = 'prompt'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    is_phantom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    item_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_groups.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_group = relationship("app.stock.item_group_domain.models.item_group.ItemGroup", foreign_keys=[item_group_id])

    qty: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    routing_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("routings.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    routing = relationship("app.manufacturing.routing_domain.models.routing.Routing", foreign_keys=[routing_id])

    rm_cost_as_per: Mapped[str] = mapped_column(SAEnum(BomCreatorRmCostAsPer, native_enum=False, length=22, validate_strings=True), nullable=False)

    set_rate_based_on_warehouse: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    buying_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    buying_price_list = relationship("app.stock.price_list_domain.models.price_list.PriceList", foreign_keys=[buying_price_list_id])

    price_list_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    plc_conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    currency: Mapped[str] = mapped_column(String(140), nullable=False)

    conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=1)

    default_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[default_warehouse_id])

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    raw_material_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(BomCreatorStatus, native_enum=False, length=15, validate_strings=True), nullable=True)

    error_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("bom_creators.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.manufacturing.bom_creator_domain.models.bom_creator.BomCreator", foreign_keys=[amended_from_id])



    items: Mapped[list["BomCreatorItem"]] = relationship(  # noqa: F821

        "app.manufacturing.bom_creator_item_domain.models.bom_creator_item.BomCreatorItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[BomCreatorItem.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BomCreator id={self.id}>"

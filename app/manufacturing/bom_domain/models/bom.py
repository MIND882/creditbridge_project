"""

BOM -- converted from ``erpnext/manufacturing/doctype/bom``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.bom_operation_domain.models.bom_operation import BomOperation

from app.manufacturing.bom_item_domain.models.bom_item import BomItem

from app.manufacturing.bom_secondary_item_domain.models.bom_secondary_item import BomSecondaryItem

from app.manufacturing.bom_explosion_item_domain.models.bom_explosion_item import BomExplosionItem

from app.manufacturing.bom_website_item_domain.models.bom_website_item import BomWebsiteItem

from app.manufacturing.bom_website_operation_domain.models.bom_website_operation import BomWebsiteOperation



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["Bom", "BomTransferMaterialAgainst", "BomBackflushBasedOn", "BomRmCostAsPer"]





class BomTransferMaterialAgainst(str, enum.Enum):

    WORK_ORDER = "Work Order"

    JOB_CARD = "Job Card"



class BomBackflushBasedOn(str, enum.Enum):

    BOM = "BOM"

    MATERIAL_TRANSFERRED_FOR_MANUFACTURE = "Material Transferred for Manufacture"



class BomRmCostAsPer(str, enum.Enum):

    VALUATION_RATE = "Valuation Rate"

    LAST_PURCHASE_RATE = "Last Purchase Rate"

    PRICE_LIST = "Price List"





class Bom(SubmittableModel, TenantModel):

    __tablename__ = "boms"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_boms_business_name"),

    )



    #: Upstream declares no ``autoname``; Frappe mints a hash.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    company: Mapped[str] = mapped_column(String(140), nullable=False)

    item_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    item = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_id])

    quantity: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=1)

    uom_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("uoms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    uom = relationship("app.stock.uom_domain.models.uom.Uom", foreign_keys=[uom_id])

    cost_allocation_per: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=100)

    cost_allocation: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    process_loss_percentage: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    process_loss_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    with_operations: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    track_semi_finished_goods: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    transfer_material_against: Mapped[Optional[str]] = mapped_column(SAEnum(BomTransferMaterialAgainst, native_enum=False, length=14, validate_strings=True), nullable=True)

    routing_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("routings.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    routing = relationship("app.manufacturing.routing_domain.models.routing.Routing", foreign_keys=[routing_id])

    fg_based_operating_cost: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    operating_cost_per_bom_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    set_rate_of_sub_assembly_item_based_on_bom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_phantom_bom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    allow_alternative_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    inspection_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    quality_inspection_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("quality_inspection_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    quality_inspection_template = relationship("app.stock.quality_inspection_template_domain.models.quality_inspection_template.QualityInspectionTemplate", foreign_keys=[quality_inspection_template_id])

    default_source_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_source_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[default_source_warehouse_id])

    default_target_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    default_target_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[default_target_warehouse_id])

    backflush_based_on: Mapped[Optional[str]] = mapped_column(SAEnum(BomBackflushBasedOn, native_enum=False, length=40, validate_strings=True), nullable=True)

    operating_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    raw_material_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    secondary_items_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_operating_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_raw_material_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_secondary_items_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    base_total_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    rm_cost_as_per: Mapped[Optional[str]] = mapped_column(SAEnum(BomRmCostAsPer, native_enum=False, length=22, validate_strings=True), nullable=True)

    buying_price_list_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("price_lists.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    buying_price_list = relationship("app.stock.price_list_domain.models.price_list.PriceList", foreign_keys=[buying_price_list_id])

    price_list_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    plc_conversion_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    currency: Mapped[str] = mapped_column(String(140), nullable=False)

    conversion_rate: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=1)

    item_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    has_variants: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    show_in_website: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    route: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    website_image: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    thumbnail: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    show_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    show_operations: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    web_long_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    bom_creator_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("bom_creators.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bom_creator = relationship("app.manufacturing.bom_creator_domain.models.bom_creator.BomCreator", foreign_keys=[bom_creator_id])

    bom_creator_item: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("boms.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.manufacturing.bom_domain.models.bom.Bom", foreign_keys=[amended_from_id])



    operations: Mapped[list["BomOperation"]] = relationship(  # noqa: F821

        "app.manufacturing.bom_operation_domain.models.bom_operation.BomOperation",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[BomOperation.parent_id],

    )



    items: Mapped[list["BomItem"]] = relationship(  # noqa: F821

        "app.manufacturing.bom_item_domain.models.bom_item.BomItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[BomItem.parent_id],

    )



    secondary_items: Mapped[list["BomSecondaryItem"]] = relationship(  # noqa: F821

        "app.manufacturing.bom_secondary_item_domain.models.bom_secondary_item.BomSecondaryItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[BomSecondaryItem.parent_id],

    )



    exploded_items: Mapped[list["BomExplosionItem"]] = relationship(  # noqa: F821

        "app.manufacturing.bom_explosion_item_domain.models.bom_explosion_item.BomExplosionItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[BomExplosionItem.parent_id],

    )



    website_items: Mapped[list["BomWebsiteItem"]] = relationship(  # noqa: F821

        "app.manufacturing.bom_website_item_domain.models.bom_website_item.BomWebsiteItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[BomWebsiteItem.parent_id],

    )



    website_operations: Mapped[list["BomWebsiteOperation"]] = relationship(  # noqa: F821

        "app.manufacturing.bom_website_operation_domain.models.bom_website_operation.BomWebsiteOperation",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[BomWebsiteOperation.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<Bom id={self.id}>"

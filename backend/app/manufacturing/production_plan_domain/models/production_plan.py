"""

Production Plan -- converted from ``erpnext/manufacturing/doctype/production_plan``.



Submittable: Draft -> Submitted -> Cancelled.

"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Numeric, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.manufacturing.production_plan_item_domain.models.production_plan_item import ProductionPlanItem

from app.manufacturing.production_plan_item_reference_domain.models.production_plan_item_reference import ProductionPlanItemReference

from app.manufacturing.production_plan_sub_assembly_item_domain.models.production_plan_sub_assembly_item import ProductionPlanSubAssemblyItem

from app.manufacturing.material_request_plan_item_domain.models.material_request_plan_item import MaterialRequestPlanItem

from app.manufacturing.production_plan_material_request_warehouse_domain.models.production_plan_material_request_warehouse import ProductionPlanMaterialRequestWarehouse



from app.core.base_model import TenantModel

from app.core.docstatus import SubmittableModel



__all__ = ["ProductionPlan", "ProductionPlanNamingSeries", "ProductionPlanGetItemsFrom", "ProductionPlanSalesOrderStatus", "ProductionPlanStatus"]





class ProductionPlanNamingSeries(str, enum.Enum):

    MFG_PP_YYYY = "MFG-PP-.YYYY.-"



class ProductionPlanGetItemsFrom(str, enum.Enum):

    SALES_ORDER = "Sales Order"

    MATERIAL_REQUEST = "Material Request"



class ProductionPlanSalesOrderStatus(str, enum.Enum):

    TO_DELIVER_AND_BILL = "To Deliver and Bill"

    TO_BILL = "To Bill"

    TO_DELIVER = "To Deliver"



class ProductionPlanStatus(str, enum.Enum):

    DRAFT = "Draft"

    SUBMITTED = "Submitted"

    NOT_STARTED = "Not Started"

    IN_PROCESS = "In Process"

    COMPLETED = "Completed"

    CLOSED = "Closed"

    CANCELLED = "Cancelled"

    MATERIAL_REQUESTED = "Material Requested"





class ProductionPlan(SubmittableModel, TenantModel):

    __tablename__ = "production_plans"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_production_plans_business_name"),

    )



    #: ``autoname`` = 'naming_series:'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    naming_series: Mapped[str] = mapped_column(SAEnum(ProductionPlanNamingSeries, native_enum=False, length=18, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=False)

    company: Mapped[str] = mapped_column(String(140), nullable=False)

    get_items_from: Mapped[Optional[str]] = mapped_column(SAEnum(ProductionPlanGetItemsFrom, native_enum=False, length=20, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    posting_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    reserve_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    item_code_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    item_code = relationship("app.stock.item_domain.models.item.Item", foreign_keys=[item_code_id])

    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("selling_customers.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    customer = relationship("app.selling.customer_domain.models.customer.Customer", foreign_keys=[customer_id])

    warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[warehouse_id])

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_order_status: Mapped[Optional[str]] = mapped_column(SAEnum(ProductionPlanSalesOrderStatus, native_enum=False, length=23, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    from_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    from_delivery_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_delivery_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    combine_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    sub_assembly_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    sub_assembly_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[sub_assembly_warehouse_id])

    skip_available_sub_assembly_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    combine_sub_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    include_non_stock_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    include_subcontracted_items: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    consider_minimum_order_qty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    include_safety_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    ignore_existing_ordered_qty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    raw_material_group_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    raw_material_group_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[raw_material_group_warehouse_id])

    for_warehouse_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("warehouses.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    for_warehouse = relationship("app.stock.warehouse_domain.models.warehouse.Warehouse", foreign_keys=[for_warehouse_id])

    total_planned_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    total_produced_qty: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True, default=0)

    status: Mapped[Optional[str]] = mapped_column(SAEnum(ProductionPlanStatus, native_enum=False, length=22, validate_strings=True, values_callable=lambda e: [m.value for m in e]), nullable=True)

    amended_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("production_plans.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    amended_from = relationship("app.manufacturing.production_plan_domain.models.production_plan.ProductionPlan", foreign_keys=[amended_from_id])



    po_items: Mapped[list["ProductionPlanItem"]] = relationship(  # noqa: F821

        "app.manufacturing.production_plan_item_domain.models.production_plan_item.ProductionPlanItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[ProductionPlanItem.parent_id],

    )



    prod_plan_references: Mapped[list["ProductionPlanItemReference"]] = relationship(  # noqa: F821

        "app.manufacturing.production_plan_item_reference_domain.models.production_plan_item_reference.ProductionPlanItemReference",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[ProductionPlanItemReference.parent_id],

    )



    sub_assembly_items: Mapped[list["ProductionPlanSubAssemblyItem"]] = relationship(  # noqa: F821

        "app.manufacturing.production_plan_sub_assembly_item_domain.models.production_plan_sub_assembly_item.ProductionPlanSubAssemblyItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[ProductionPlanSubAssemblyItem.parent_id],

    )



    mr_items: Mapped[list["MaterialRequestPlanItem"]] = relationship(  # noqa: F821

        "app.manufacturing.material_request_plan_item_domain.models.material_request_plan_item.MaterialRequestPlanItem",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[MaterialRequestPlanItem.parent_id],

    )



    warehouses: Mapped[list["ProductionPlanMaterialRequestWarehouse"]] = relationship(  # noqa: F821

        "app.manufacturing.production_plan_material_request_warehouse_domain.models.production_plan_material_request_warehouse.ProductionPlanMaterialRequestWarehouse",

        back_populates="parent",

        # explicit: a child may hold a second FK back to this same

        # table, which would make the join ambiguous

        cascade="all, delete-orphan",

        foreign_keys=[ProductionPlanMaterialRequestWarehouse.parent_id],

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProductionPlan id={self.id}>"

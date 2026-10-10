"""Pydantic v2 schemas for ProductionPlan."""





from __future__ import annotations

from app.manufacturing.production_plan_domain.models.production_plan import (

    ProductionPlanNamingSeries,

    ProductionPlanGetItemsFrom,

    ProductionPlanSalesOrderStatus,

    ProductionPlanStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.manufacturing.production_plan_item_domain.schemas.production_plan_item import (

    ProductionPlanItemCreate,

    ProductionPlanItemRead,

)

from app.manufacturing.production_plan_item_reference_domain.schemas.production_plan_item_reference import (

    ProductionPlanItemReferenceCreate,

    ProductionPlanItemReferenceRead,

)

from app.manufacturing.production_plan_sub_assembly_item_domain.schemas.production_plan_sub_assembly_item import (

    ProductionPlanSubAssemblyItemCreate,

    ProductionPlanSubAssemblyItemRead,

)

from app.manufacturing.material_request_plan_item_domain.schemas.material_request_plan_item import (

    MaterialRequestPlanItemCreate,

    MaterialRequestPlanItemRead,

)

from app.manufacturing.production_plan_material_request_warehouse_domain.schemas.production_plan_material_request_warehouse import (

    ProductionPlanMaterialRequestWarehouseCreate,

    ProductionPlanMaterialRequestWarehouseRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProductionPlanCreate",

    "ProductionPlanUpdate",

    "ProductionPlanRead",

    "ProductionPlanListResponse",

]





class ProductionPlanBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: ProductionPlanNamingSeries

    company: str

    get_items_from: Optional[ProductionPlanGetItemsFrom] = None

    posting_date: dt.date

    reserve_stock: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None

    customer_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    sales_order_status: Optional[ProductionPlanSalesOrderStatus] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    from_delivery_date: Optional[dt.date] = None

    to_delivery_date: Optional[dt.date] = None

    combine_items: Optional[bool] = None

    sub_assembly_warehouse_id: Optional[uuid.UUID] = None

    skip_available_sub_assembly_item: Optional[bool] = None

    combine_sub_items: Optional[bool] = None

    include_non_stock_items: Optional[bool] = None

    include_subcontracted_items: Optional[bool] = None

    consider_minimum_order_qty: Optional[bool] = None

    include_safety_stock: Optional[bool] = None

    ignore_existing_ordered_qty: Optional[bool] = None

    raw_material_group_warehouse_id: Optional[uuid.UUID] = None

    for_warehouse_id: Optional[uuid.UUID] = None

    total_planned_qty: Optional[Decimal] = None

    total_produced_qty: Optional[Decimal] = None

    status: Optional[ProductionPlanStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    po_items: list[ProductionPlanItemCreate] = []

    prod_plan_references: list[ProductionPlanItemReferenceCreate] = []

    sub_assembly_items: list[ProductionPlanSubAssemblyItemCreate] = []

    mr_items: list[MaterialRequestPlanItemCreate] = []

    warehouses: list[ProductionPlanMaterialRequestWarehouseCreate] = []





class ProductionPlanCreate(ProductionPlanBase):

    pass





class ProductionPlanUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[ProductionPlanNamingSeries] = None

    company: Optional[str] = None

    get_items_from: Optional[ProductionPlanGetItemsFrom] = None

    posting_date: Optional[dt.date] = None

    reserve_stock: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None

    customer_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    sales_order_status: Optional[ProductionPlanSalesOrderStatus] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    from_delivery_date: Optional[dt.date] = None

    to_delivery_date: Optional[dt.date] = None

    combine_items: Optional[bool] = None

    sub_assembly_warehouse_id: Optional[uuid.UUID] = None

    skip_available_sub_assembly_item: Optional[bool] = None

    combine_sub_items: Optional[bool] = None

    include_non_stock_items: Optional[bool] = None

    include_subcontracted_items: Optional[bool] = None

    consider_minimum_order_qty: Optional[bool] = None

    include_safety_stock: Optional[bool] = None

    ignore_existing_ordered_qty: Optional[bool] = None

    raw_material_group_warehouse_id: Optional[uuid.UUID] = None

    for_warehouse_id: Optional[uuid.UUID] = None

    total_planned_qty: Optional[Decimal] = None

    total_produced_qty: Optional[Decimal] = None

    status: Optional[ProductionPlanStatus] = None

    amended_from_id: Optional[uuid.UUID] = None

    po_items: Optional[list[ProductionPlanItemCreate]] = None

    prod_plan_references: Optional[list[ProductionPlanItemReferenceCreate]] = None

    sub_assembly_items: Optional[list[ProductionPlanSubAssemblyItemCreate]] = None

    mr_items: Optional[list[MaterialRequestPlanItemCreate]] = None

    warehouses: Optional[list[ProductionPlanMaterialRequestWarehouseCreate]] = None





class ProductionPlanRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[ProductionPlanNamingSeries] = None

    company: str

    get_items_from: Optional[ProductionPlanGetItemsFrom] = None

    posting_date: Optional[dt.date] = None

    reserve_stock: Optional[bool] = None

    item_code_id: Optional[uuid.UUID] = None

    customer_id: Optional[uuid.UUID] = None

    warehouse_id: Optional[uuid.UUID] = None

    project: Optional[str] = None

    sales_order_status: Optional[ProductionPlanSalesOrderStatus] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    from_delivery_date: Optional[dt.date] = None

    to_delivery_date: Optional[dt.date] = None

    combine_items: Optional[bool] = None

    sub_assembly_warehouse_id: Optional[uuid.UUID] = None

    skip_available_sub_assembly_item: Optional[bool] = None

    combine_sub_items: Optional[bool] = None

    include_non_stock_items: Optional[bool] = None

    include_subcontracted_items: Optional[bool] = None

    consider_minimum_order_qty: Optional[bool] = None

    include_safety_stock: Optional[bool] = None

    ignore_existing_ordered_qty: Optional[bool] = None

    raw_material_group_warehouse_id: Optional[uuid.UUID] = None

    for_warehouse_id: Optional[uuid.UUID] = None

    total_planned_qty: Optional[Decimal] = None

    total_produced_qty: Optional[Decimal] = None

    status: Optional[ProductionPlanStatus] = None

    amended_from_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    po_items: list[ProductionPlanItemRead] = []

    prod_plan_references: list[ProductionPlanItemReferenceRead] = []

    sub_assembly_items: list[ProductionPlanSubAssemblyItemRead] = []

    mr_items: list[MaterialRequestPlanItemRead] = []

    warehouses: list[ProductionPlanMaterialRequestWarehouseRead] = []





ProductionPlanListResponse = Page[ProductionPlanRead]

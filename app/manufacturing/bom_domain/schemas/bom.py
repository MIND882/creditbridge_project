"""Pydantic v2 schemas for Bom."""





from __future__ import annotations

from app.manufacturing.bom_domain.models.bom import (

    BomTransferMaterialAgainst,

    BomBackflushBasedOn,

    BomRmCostAsPer,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.manufacturing.bom_operation_domain.schemas.bom_operation import (

    BomOperationCreate,

    BomOperationRead,

)

from app.manufacturing.bom_item_domain.schemas.bom_item import (

    BomItemCreate,

    BomItemRead,

)

from app.manufacturing.bom_secondary_item_domain.schemas.bom_secondary_item import (

    BomSecondaryItemCreate,

    BomSecondaryItemRead,

)

from app.manufacturing.bom_explosion_item_domain.schemas.bom_explosion_item import (

    BomExplosionItemCreate,

    BomExplosionItemRead,

)

from app.manufacturing.bom_website_item_domain.schemas.bom_website_item import (

    BomWebsiteItemCreate,

    BomWebsiteItemRead,

)

from app.manufacturing.bom_website_operation_domain.schemas.bom_website_operation import (

    BomWebsiteOperationCreate,

    BomWebsiteOperationRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomCreate",

    "BomUpdate",

    "BomRead",

    "BomListResponse",

]





class BomBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: str

    item_id: uuid.UUID

    quantity: Decimal

    uom_id: Optional[uuid.UUID] = None

    cost_allocation_per: Optional[Decimal] = None

    cost_allocation: Optional[Decimal] = None

    process_loss_percentage: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    with_operations: Optional[bool] = None

    track_semi_finished_goods: Optional[bool] = None

    transfer_material_against: Optional[BomTransferMaterialAgainst] = None

    routing_id: Optional[uuid.UUID] = None

    fg_based_operating_cost: Optional[bool] = None

    operating_cost_per_bom_quantity: Optional[Decimal] = None

    is_active: Optional[bool] = None

    is_default: Optional[bool] = None

    set_rate_of_sub_assembly_item_based_on_bom: Optional[bool] = None

    is_phantom_bom: Optional[bool] = None

    allow_alternative_item: Optional[bool] = None

    inspection_required: Optional[bool] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    default_source_warehouse_id: Optional[uuid.UUID] = None

    default_target_warehouse_id: Optional[uuid.UUID] = None

    backflush_based_on: Optional[BomBackflushBasedOn] = None

    operating_cost: Optional[Decimal] = None

    raw_material_cost: Optional[Decimal] = None

    secondary_items_cost: Optional[Decimal] = None

    base_operating_cost: Optional[Decimal] = None

    base_raw_material_cost: Optional[Decimal] = None

    base_secondary_items_cost: Optional[Decimal] = None

    total_cost: Optional[Decimal] = None

    base_total_cost: Optional[Decimal] = None

    rm_cost_as_per: Optional[BomRmCostAsPer] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    currency: str

    conversion_rate: Decimal

    item_name: Optional[str] = None

    image: Optional[str] = None

    description: Optional[str] = None

    has_variants: Optional[bool] = None

    project: Optional[str] = None

    show_in_website: Optional[bool] = None

    route: Optional[str] = None

    website_image: Optional[str] = None

    thumbnail: Optional[str] = None

    show_items: Optional[bool] = None

    show_operations: Optional[bool] = None

    web_long_description: Optional[str] = None

    bom_creator_id: Optional[uuid.UUID] = None

    bom_creator_item: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    operations: list[BomOperationCreate] = []

    items: list[BomItemCreate] = []

    secondary_items: list[BomSecondaryItemCreate] = []

    exploded_items: list[BomExplosionItemCreate] = []

    website_items: list[BomWebsiteItemCreate] = []

    website_operations: list[BomWebsiteOperationCreate] = []





class BomCreate(BomBase):

    pass





class BomUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None

    item_id: Optional[uuid.UUID] = None

    quantity: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    cost_allocation_per: Optional[Decimal] = None

    cost_allocation: Optional[Decimal] = None

    process_loss_percentage: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    with_operations: Optional[bool] = None

    track_semi_finished_goods: Optional[bool] = None

    transfer_material_against: Optional[BomTransferMaterialAgainst] = None

    routing_id: Optional[uuid.UUID] = None

    fg_based_operating_cost: Optional[bool] = None

    operating_cost_per_bom_quantity: Optional[Decimal] = None

    is_active: Optional[bool] = None

    is_default: Optional[bool] = None

    set_rate_of_sub_assembly_item_based_on_bom: Optional[bool] = None

    is_phantom_bom: Optional[bool] = None

    allow_alternative_item: Optional[bool] = None

    inspection_required: Optional[bool] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    default_source_warehouse_id: Optional[uuid.UUID] = None

    default_target_warehouse_id: Optional[uuid.UUID] = None

    backflush_based_on: Optional[BomBackflushBasedOn] = None

    operating_cost: Optional[Decimal] = None

    raw_material_cost: Optional[Decimal] = None

    secondary_items_cost: Optional[Decimal] = None

    base_operating_cost: Optional[Decimal] = None

    base_raw_material_cost: Optional[Decimal] = None

    base_secondary_items_cost: Optional[Decimal] = None

    total_cost: Optional[Decimal] = None

    base_total_cost: Optional[Decimal] = None

    rm_cost_as_per: Optional[BomRmCostAsPer] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    currency: Optional[str] = None

    conversion_rate: Optional[Decimal] = None

    item_name: Optional[str] = None

    image: Optional[str] = None

    description: Optional[str] = None

    has_variants: Optional[bool] = None

    project: Optional[str] = None

    show_in_website: Optional[bool] = None

    route: Optional[str] = None

    website_image: Optional[str] = None

    thumbnail: Optional[str] = None

    show_items: Optional[bool] = None

    show_operations: Optional[bool] = None

    web_long_description: Optional[str] = None

    bom_creator_id: Optional[uuid.UUID] = None

    bom_creator_item: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    operations: Optional[list[BomOperationCreate]] = None

    items: Optional[list[BomItemCreate]] = None

    secondary_items: Optional[list[BomSecondaryItemCreate]] = None

    exploded_items: Optional[list[BomExplosionItemCreate]] = None

    website_items: Optional[list[BomWebsiteItemCreate]] = None

    website_operations: Optional[list[BomWebsiteOperationCreate]] = None





class BomRead(ReadSchema):

    id: uuid.UUID

    name: str

    company: str

    item_id: Optional[uuid.UUID] = None

    quantity: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None

    cost_allocation_per: Optional[Decimal] = None

    cost_allocation: Optional[Decimal] = None

    process_loss_percentage: Optional[Decimal] = None

    process_loss_qty: Optional[Decimal] = None

    with_operations: Optional[bool] = None

    track_semi_finished_goods: Optional[bool] = None

    transfer_material_against: Optional[BomTransferMaterialAgainst] = None

    routing_id: Optional[uuid.UUID] = None

    fg_based_operating_cost: Optional[bool] = None

    operating_cost_per_bom_quantity: Optional[Decimal] = None

    is_active: Optional[bool] = None

    is_default: Optional[bool] = None

    set_rate_of_sub_assembly_item_based_on_bom: Optional[bool] = None

    is_phantom_bom: Optional[bool] = None

    allow_alternative_item: Optional[bool] = None

    inspection_required: Optional[bool] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    default_source_warehouse_id: Optional[uuid.UUID] = None

    default_target_warehouse_id: Optional[uuid.UUID] = None

    backflush_based_on: Optional[BomBackflushBasedOn] = None

    operating_cost: Optional[Decimal] = None

    raw_material_cost: Optional[Decimal] = None

    secondary_items_cost: Optional[Decimal] = None

    base_operating_cost: Optional[Decimal] = None

    base_raw_material_cost: Optional[Decimal] = None

    base_secondary_items_cost: Optional[Decimal] = None

    total_cost: Optional[Decimal] = None

    base_total_cost: Optional[Decimal] = None

    rm_cost_as_per: Optional[BomRmCostAsPer] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    price_list_currency: Optional[str] = None

    plc_conversion_rate: Optional[Decimal] = None

    currency: str

    conversion_rate: Optional[Decimal] = None

    item_name: Optional[str] = None

    image: Optional[str] = None

    description: Optional[str] = None

    has_variants: Optional[bool] = None

    project: Optional[str] = None

    show_in_website: Optional[bool] = None

    route: Optional[str] = None

    website_image: Optional[str] = None

    thumbnail: Optional[str] = None

    show_items: Optional[bool] = None

    show_operations: Optional[bool] = None

    web_long_description: Optional[str] = None

    bom_creator_id: Optional[uuid.UUID] = None

    bom_creator_item: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    operations: list[BomOperationRead] = []

    items: list[BomItemRead] = []

    secondary_items: list[BomSecondaryItemRead] = []

    exploded_items: list[BomExplosionItemRead] = []

    website_items: list[BomWebsiteItemRead] = []

    website_operations: list[BomWebsiteOperationRead] = []





BomListResponse = Page[BomRead]

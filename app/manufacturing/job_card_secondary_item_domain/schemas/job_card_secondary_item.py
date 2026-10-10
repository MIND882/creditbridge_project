"""Pydantic v2 schemas for JobCardSecondaryItem."""





from __future__ import annotations

from app.manufacturing.job_card_secondary_item_domain.models.job_card_secondary_item import (

    JobCardSecondaryItemSecondaryItemType,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "JobCardSecondaryItemCreate",

    "JobCardSecondaryItemRead",

    "JobCardSecondaryItemListResponse",

]





class JobCardSecondaryItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    secondary_item_type: JobCardSecondaryItemSecondaryItemType

    description: Optional[str] = None

    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    bom_secondary_item: Optional[str] = None

    stock_qty: Decimal

    stock_uom_id: Optional[uuid.UUID] = None





class JobCardSecondaryItemCreate(JobCardSecondaryItemBase):

    pass





class JobCardSecondaryItemUpdate(InputSchema):

    """A partial update."""



    secondary_item_type: Optional[JobCardSecondaryItemSecondaryItemType] = None

    description: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    bom_secondary_item: Optional[str] = None

    stock_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None





class JobCardSecondaryItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    secondary_item_type: Optional[JobCardSecondaryItemSecondaryItemType] = None

    description: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    bom_secondary_item: Optional[str] = None

    stock_qty: Optional[Decimal] = None

    stock_uom_id: Optional[uuid.UUID] = None





JobCardSecondaryItemListResponse = Page[JobCardSecondaryItemRead]

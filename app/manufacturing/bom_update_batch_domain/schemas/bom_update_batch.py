"""Pydantic v2 schemas for BomUpdateBatch."""





from __future__ import annotations

from app.manufacturing.bom_update_batch_domain.models.bom_update_batch import (

    BomUpdateBatchStatus,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomUpdateBatchCreate",

    "BomUpdateBatchRead",

    "BomUpdateBatchListResponse",

]





class BomUpdateBatchBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    level: Optional[int] = None

    batch_no: Optional[int] = None

    boms_updated: Optional[str] = None

    status: Optional[BomUpdateBatchStatus] = None





class BomUpdateBatchCreate(BomUpdateBatchBase):

    pass





class BomUpdateBatchUpdate(InputSchema):

    """A partial update."""



    level: Optional[int] = None

    batch_no: Optional[int] = None

    boms_updated: Optional[str] = None

    status: Optional[BomUpdateBatchStatus] = None





class BomUpdateBatchRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    level: Optional[int] = None

    batch_no: Optional[int] = None

    boms_updated: Optional[str] = None

    status: Optional[BomUpdateBatchStatus] = None





BomUpdateBatchListResponse = Page[BomUpdateBatchRead]

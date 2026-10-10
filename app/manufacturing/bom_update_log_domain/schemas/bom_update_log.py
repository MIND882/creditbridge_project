"""Pydantic v2 schemas for BomUpdateLog."""





from __future__ import annotations

from app.manufacturing.bom_update_log_domain.models.bom_update_log import (

    BomUpdateLogUpdateType,

    BomUpdateLogStatus,

)

from typing import Optional

import uuid



from app.manufacturing.bom_update_batch_domain.schemas.bom_update_batch import (

    BomUpdateBatchCreate,

    BomUpdateBatchRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomUpdateLogCreate",

    "BomUpdateLogUpdate",

    "BomUpdateLogRead",

    "BomUpdateLogListResponse",

]





class BomUpdateLogBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    update_type: Optional[BomUpdateLogUpdateType] = None

    status: Optional[BomUpdateLogStatus] = None

    current_bom_id: Optional[uuid.UUID] = None

    new_bom_id: Optional[uuid.UUID] = None

    error_log: Optional[str] = None

    current_level: Optional[int] = None

    processed_boms: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    bom_batches: list[BomUpdateBatchCreate] = []





class BomUpdateLogCreate(BomUpdateLogBase):

    pass





class BomUpdateLogUpdate(InputSchema):

    """A partial update."""



    update_type: Optional[BomUpdateLogUpdateType] = None

    status: Optional[BomUpdateLogStatus] = None

    current_bom_id: Optional[uuid.UUID] = None

    new_bom_id: Optional[uuid.UUID] = None

    error_log: Optional[str] = None

    current_level: Optional[int] = None

    processed_boms: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    bom_batches: Optional[list[BomUpdateBatchCreate]] = None





class BomUpdateLogRead(ReadSchema):

    id: uuid.UUID

    name: str

    update_type: Optional[BomUpdateLogUpdateType] = None

    status: Optional[BomUpdateLogStatus] = None

    current_bom_id: Optional[uuid.UUID] = None

    new_bom_id: Optional[uuid.UUID] = None

    error_log: Optional[str] = None

    current_level: Optional[int] = None

    processed_boms: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    bom_batches: list[BomUpdateBatchRead] = []





BomUpdateLogListResponse = Page[BomUpdateLogRead]

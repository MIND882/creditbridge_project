"""Pydantic v2 schemas for JobCardOperation."""





from __future__ import annotations

from app.manufacturing.job_card_operation_domain.models.job_card_operation import (

    JobCardOperationStatus,

)

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "JobCardOperationCreate",

    "JobCardOperationRead",

    "JobCardOperationListResponse",

]





class JobCardOperationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    sub_operation_id: Optional[uuid.UUID] = None

    completed_qty: Optional[Decimal] = None

    completed_time: Optional[str] = None

    status: Optional[JobCardOperationStatus] = None





class JobCardOperationCreate(JobCardOperationBase):

    pass





class JobCardOperationUpdate(InputSchema):

    """A partial update."""



    sub_operation_id: Optional[uuid.UUID] = None

    completed_qty: Optional[Decimal] = None

    completed_time: Optional[str] = None

    status: Optional[JobCardOperationStatus] = None





class JobCardOperationRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    sub_operation_id: Optional[uuid.UUID] = None

    completed_qty: Optional[Decimal] = None

    completed_time: Optional[str] = None

    status: Optional[JobCardOperationStatus] = None





JobCardOperationListResponse = Page[JobCardOperationRead]

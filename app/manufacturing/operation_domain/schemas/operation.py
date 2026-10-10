"""Pydantic v2 schemas for Operation."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.manufacturing.sub_operation_domain.schemas.sub_operation import (

    SubOperationCreate,

    SubOperationRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "OperationCreate",

    "OperationUpdate",

    "OperationRead",

    "OperationListResponse",

]





class OperationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    workstation_id: Optional[uuid.UUID] = None

    is_corrective_operation: Optional[bool] = None

    create_job_card_based_on_batch_size: Optional[bool] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    batch_size: Optional[int] = None

    total_operation_time: Optional[Decimal] = None

    description: Optional[str] = None

    work_instruction: Optional[str] = None

    sub_operations: list[SubOperationCreate] = []





class OperationCreate(OperationBase):

    pass





class OperationUpdate(InputSchema):

    """A partial update."""



    workstation_id: Optional[uuid.UUID] = None

    is_corrective_operation: Optional[bool] = None

    create_job_card_based_on_batch_size: Optional[bool] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    batch_size: Optional[int] = None

    total_operation_time: Optional[Decimal] = None

    description: Optional[str] = None

    work_instruction: Optional[str] = None

    sub_operations: Optional[list[SubOperationCreate]] = None





class OperationRead(ReadSchema):

    id: uuid.UUID

    name: str

    workstation_id: Optional[uuid.UUID] = None

    is_corrective_operation: Optional[bool] = None

    create_job_card_based_on_batch_size: Optional[bool] = None

    quality_inspection_template_id: Optional[uuid.UUID] = None

    batch_size: Optional[int] = None

    total_operation_time: Optional[Decimal] = None

    description: Optional[str] = None

    work_instruction: Optional[str] = None

    sub_operations: list[SubOperationRead] = []





OperationListResponse = Page[OperationRead]

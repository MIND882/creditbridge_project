"""Pydantic v2 schemas for ProcessPaymentReconciliationLog."""





from __future__ import annotations

from app.accounts.process_payment_reconciliation_log_domain.models.process_payment_reconciliation_log import (

    ProcessPaymentReconciliationLogStatus,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.process_payment_reconciliation_log_allocations_domain.schemas.process_payment_reconciliation_log_allocations import (

    ProcessPaymentReconciliationLogAllocationsCreate,

    ProcessPaymentReconciliationLogAllocationsRead,

)



__all__ = [

    "ProcessPaymentReconciliationLogCreate",

    "ProcessPaymentReconciliationLogUpdate",

    "ProcessPaymentReconciliationLogRead",

    "ProcessPaymentReconciliationLogListResponse",

]





class ProcessPaymentReconciliationLogBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    reconciled: Optional[bool] = None

    total_allocations: Optional[int] = None

    allocated: Optional[bool] = None

    reconciled_entries: Optional[int] = None

    error_log: Optional[str] = None

    process_pr: str

    status: Optional[ProcessPaymentReconciliationLogStatus] = None



    allocations: list[ProcessPaymentReconciliationLogAllocationsCreate] = []





class ProcessPaymentReconciliationLogCreate(ProcessPaymentReconciliationLogBase):

    pass





class ProcessPaymentReconciliationLogUpdate(InputSchema):

    """A partial update."""



    reconciled: Optional[bool] = None

    total_allocations: Optional[int] = None

    allocated: Optional[bool] = None

    reconciled_entries: Optional[int] = None

    error_log: Optional[str] = None

    process_pr: Optional[str] = None

    status: Optional[ProcessPaymentReconciliationLogStatus] = None

    allocations: Optional[list[ProcessPaymentReconciliationLogAllocationsCreate]] = None





class ProcessPaymentReconciliationLogRead(ReadSchema):

    id: uuid.UUID

    name: str

    reconciled: bool

    total_allocations: Optional[int] = None

    allocated: bool

    reconciled_entries: Optional[int] = None

    error_log: Optional[str] = None

    process_pr: str

    status: Optional[ProcessPaymentReconciliationLogStatus] = None

    allocations: list[ProcessPaymentReconciliationLogAllocationsRead] = []





ProcessPaymentReconciliationLogListResponse = Page[ProcessPaymentReconciliationLogRead]

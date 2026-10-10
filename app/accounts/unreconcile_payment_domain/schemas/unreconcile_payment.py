"""Pydantic v2 schemas for UnreconcilePayment."""





from __future__ import annotations

from typing import Optional

import uuid



from app.accounts.unreconcile_payment_entries_domain.schemas.unreconcile_payment_entries import (

    UnreconcilePaymentEntriesCreate,

    UnreconcilePaymentEntriesRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.process_payment_reconciliation_log_allocations_domain.schemas.process_payment_reconciliation_log_allocations import (

    ProcessPaymentReconciliationLogAllocationsCreate,

    ProcessPaymentReconciliationLogAllocationsRead,

)



__all__ = [

    "UnreconcilePaymentCreate",

    "UnreconcilePaymentUpdate",

    "UnreconcilePaymentRead",

    "UnreconcilePaymentListResponse",

]





class UnreconcilePaymentBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    amended_from: Optional[str] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None



    allocations: list[UnreconcilePaymentEntriesCreate] = []





class UnreconcilePaymentCreate(UnreconcilePaymentBase):

    pass





class UnreconcilePaymentUpdate(InputSchema):

    """A partial update."""



    amended_from: Optional[str] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    allocations: Optional[list[UnreconcilePaymentEntriesCreate]] = None





class UnreconcilePaymentRead(ReadSchema):

    id: uuid.UUID

    name: str

    amended_from: Optional[str] = None

    voucher_type: Optional[str] = None

    voucher_no: Optional[str] = None

    allocations: list[UnreconcilePaymentEntriesRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





UnreconcilePaymentListResponse = Page[UnreconcilePaymentRead]

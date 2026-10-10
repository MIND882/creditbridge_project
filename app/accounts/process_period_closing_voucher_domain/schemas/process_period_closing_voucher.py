"""Pydantic v2 schemas for ProcessPeriodClosingVoucher."""





from __future__ import annotations

from app.accounts.process_period_closing_voucher_domain.models.process_period_closing_voucher import (

    ProcessPeriodClosingVoucherStatus,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.process_period_closing_voucher_detail_domain.schemas.process_period_closing_voucher_detail import (

    ProcessPeriodClosingVoucherDetailCreate,

    ProcessPeriodClosingVoucherDetailRead,

)

from app.accounts.process_period_closing_voucher_detail_domain.schemas.process_period_closing_voucher_detail import (

    ProcessPeriodClosingVoucherDetailCreate,

    ProcessPeriodClosingVoucherDetailRead,

)



__all__ = [

    "ProcessPeriodClosingVoucherCreate",

    "ProcessPeriodClosingVoucherUpdate",

    "ProcessPeriodClosingVoucherRead",

    "ProcessPeriodClosingVoucherListResponse",

]





class ProcessPeriodClosingVoucherBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    parent_pcv: str

    status: Optional[ProcessPeriodClosingVoucherStatus] = None

    amended_from: Optional[str] = None

    p_l_closing_balance: Optional[str] = None

    bs_closing_balance: Optional[str] = None



    normal_balances: list[ProcessPeriodClosingVoucherDetailCreate] = []



    z_opening_balances: list[ProcessPeriodClosingVoucherDetailCreate] = []





class ProcessPeriodClosingVoucherCreate(ProcessPeriodClosingVoucherBase):

    pass





class ProcessPeriodClosingVoucherUpdate(InputSchema):

    """A partial update."""



    parent_pcv: Optional[str] = None

    status: Optional[ProcessPeriodClosingVoucherStatus] = None

    amended_from: Optional[str] = None

    p_l_closing_balance: Optional[str] = None

    bs_closing_balance: Optional[str] = None

    normal_balances: Optional[list[ProcessPeriodClosingVoucherDetailCreate]] = None

    z_opening_balances: Optional[list[ProcessPeriodClosingVoucherDetailCreate]] = None





class ProcessPeriodClosingVoucherRead(ReadSchema):

    id: uuid.UUID

    name: str

    parent_pcv: str

    status: Optional[ProcessPeriodClosingVoucherStatus] = None

    amended_from: Optional[str] = None

    p_l_closing_balance: Optional[str] = None

    bs_closing_balance: Optional[str] = None

    normal_balances: list[ProcessPeriodClosingVoucherDetailRead] = []

    z_opening_balances: list[ProcessPeriodClosingVoucherDetailRead] = []



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0





ProcessPeriodClosingVoucherListResponse = Page[ProcessPeriodClosingVoucherRead]

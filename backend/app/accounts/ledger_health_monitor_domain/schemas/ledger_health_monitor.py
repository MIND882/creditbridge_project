"""Pydantic v2 schemas for LedgerHealthMonitor."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.ledger_health_monitor_company_domain.schemas.ledger_health_monitor_company import (

    LedgerHealthMonitorCompanyCreate,

    LedgerHealthMonitorCompanyRead,

)



__all__ = [

    "LedgerHealthMonitorCreate",

    "LedgerHealthMonitorUpdate",

    "LedgerHealthMonitorRead",

    "LedgerHealthMonitorListResponse",

]





class LedgerHealthMonitorBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    enable_health_monitor: Optional[bool] = None

    debit_credit_mismatch: Optional[bool] = None

    general_and_payment_ledger_mismatch: Optional[bool] = None

    monitor_for_last_x_days: Optional[int] = None



    companies: list[LedgerHealthMonitorCompanyCreate] = []





class LedgerHealthMonitorCreate(LedgerHealthMonitorBase):

    pass





class LedgerHealthMonitorUpdate(InputSchema):

    """A partial update."""



    enable_health_monitor: Optional[bool] = None

    debit_credit_mismatch: Optional[bool] = None

    general_and_payment_ledger_mismatch: Optional[bool] = None

    monitor_for_last_x_days: Optional[int] = None

    companies: Optional[list[LedgerHealthMonitorCompanyCreate]] = None





class LedgerHealthMonitorRead(ReadSchema):

    id: uuid.UUID

    name: str

    enable_health_monitor: bool

    debit_credit_mismatch: bool

    general_and_payment_ledger_mismatch: bool

    monitor_for_last_x_days: int

    companies: list[LedgerHealthMonitorCompanyRead] = []





LedgerHealthMonitorListResponse = Page[LedgerHealthMonitorRead]

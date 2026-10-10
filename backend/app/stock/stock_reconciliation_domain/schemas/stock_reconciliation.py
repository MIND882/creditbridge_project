"""Pydantic v2 schemas for StockReconciliation."""





from __future__ import annotations

from app.stock.stock_reconciliation_domain.models.stock_reconciliation import (

    StockReconciliationNamingSeries,

    StockReconciliationPurpose,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.stock_reconciliation_item_domain.schemas.stock_reconciliation_item import (

    StockReconciliationItemCreate,

    StockReconciliationItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockReconciliationCreate",

    "StockReconciliationUpdate",

    "StockReconciliationRead",

    "StockReconciliationListResponse",

]





class StockReconciliationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: StockReconciliationNamingSeries

    company: str

    purpose: StockReconciliationPurpose

    posting_date: dt.date

    posting_time: dt.time

    set_posting_time: Optional[bool] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    difference_amount: Optional[Decimal] = None

    amended_from_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    scan_mode: Optional[bool] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    last_scanned_warehouse: Optional[str] = None

    items: list[StockReconciliationItemCreate] = []





class StockReconciliationCreate(StockReconciliationBase):

    pass





class StockReconciliationUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[StockReconciliationNamingSeries] = None

    company: Optional[str] = None

    purpose: Optional[StockReconciliationPurpose] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    difference_amount: Optional[Decimal] = None

    amended_from_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    scan_mode: Optional[bool] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    last_scanned_warehouse: Optional[str] = None

    items: Optional[list[StockReconciliationItemCreate]] = None





class StockReconciliationRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[StockReconciliationNamingSeries] = None

    company: str

    purpose: Optional[StockReconciliationPurpose] = None

    posting_date: Optional[dt.date] = None

    posting_time: Optional[dt.time] = None

    set_posting_time: Optional[bool] = None

    expense_account_id: Optional[uuid.UUID] = None

    cost_center_id: Optional[uuid.UUID] = None

    difference_amount: Optional[Decimal] = None

    amended_from_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    scan_mode: Optional[bool] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    last_scanned_warehouse: Optional[str] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[StockReconciliationItemRead] = []





StockReconciliationListResponse = Page[StockReconciliationRead]

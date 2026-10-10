"""Pydantic v2 schemas for MaterialRequest."""





from __future__ import annotations

from app.stock.material_request_domain.models.material_request import (

    MaterialRequestNamingSeries,

    MaterialRequestMaterialRequestType,

    MaterialRequestStatus,

    MaterialRequestTransferStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.stock.material_request_item_domain.schemas.material_request_item import (

    MaterialRequestItemCreate,

    MaterialRequestItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "MaterialRequestCreate",

    "MaterialRequestUpdate",

    "MaterialRequestRead",

    "MaterialRequestListResponse",

]





class MaterialRequestBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    naming_series: MaterialRequestNamingSeries

    title: Optional[str] = None

    material_request_type: MaterialRequestMaterialRequestType

    customer: Optional[str] = None

    schedule_date: Optional[dt.date] = None

    company: str

    amended_from_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    transaction_date: dt.date

    status: Optional[MaterialRequestStatus] = None

    per_ordered: Optional[Decimal] = None

    per_received: Optional[Decimal] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    job_card: Optional[str] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    set_from_warehouse_id: Optional[uuid.UUID] = None

    transfer_status: Optional[MaterialRequestTransferStatus] = None

    work_order: Optional[str] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    last_scanned_warehouse: Optional[str] = None

    auto_created_via_reorder: Optional[bool] = None

    items: list[MaterialRequestItemCreate] = []





class MaterialRequestCreate(MaterialRequestBase):

    pass





class MaterialRequestUpdate(InputSchema):

    """A partial update."""



    naming_series: Optional[MaterialRequestNamingSeries] = None

    title: Optional[str] = None

    material_request_type: Optional[MaterialRequestMaterialRequestType] = None

    customer: Optional[str] = None

    schedule_date: Optional[dt.date] = None

    company: Optional[str] = None

    amended_from_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    transaction_date: Optional[dt.date] = None

    status: Optional[MaterialRequestStatus] = None

    per_ordered: Optional[Decimal] = None

    per_received: Optional[Decimal] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    job_card: Optional[str] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    set_from_warehouse_id: Optional[uuid.UUID] = None

    transfer_status: Optional[MaterialRequestTransferStatus] = None

    work_order: Optional[str] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    last_scanned_warehouse: Optional[str] = None

    auto_created_via_reorder: Optional[bool] = None

    items: Optional[list[MaterialRequestItemCreate]] = None





class MaterialRequestRead(ReadSchema):

    id: uuid.UUID

    name: str

    naming_series: Optional[MaterialRequestNamingSeries] = None

    title: Optional[str] = None

    material_request_type: Optional[MaterialRequestMaterialRequestType] = None

    customer: Optional[str] = None

    schedule_date: Optional[dt.date] = None

    company: str

    amended_from_id: Optional[uuid.UUID] = None

    scan_barcode: Optional[str] = None

    transaction_date: Optional[dt.date] = None

    status: Optional[MaterialRequestStatus] = None

    per_ordered: Optional[Decimal] = None

    per_received: Optional[Decimal] = None

    letter_head: Optional[str] = None

    select_print_heading: Optional[str] = None

    tc_name: Optional[str] = None

    terms: Optional[str] = None

    job_card: Optional[str] = None

    set_warehouse_id: Optional[uuid.UUID] = None

    set_from_warehouse_id: Optional[uuid.UUID] = None

    transfer_status: Optional[MaterialRequestTransferStatus] = None

    work_order: Optional[str] = None

    buying_price_list_id: Optional[uuid.UUID] = None

    last_scanned_warehouse: Optional[str] = None

    auto_created_via_reorder: Optional[bool] = None



    #: Workflow state: 0 Draft, 1 Submitted, 2 Cancelled.

    #: Clients need this to render the submit/cancel affordances. It is

    #: derived from the document and never accepted on input.

    docstatus: int = 0

    items: list[MaterialRequestItemRead] = []





MaterialRequestListResponse = Page[MaterialRequestRead]

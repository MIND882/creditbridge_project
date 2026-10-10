"""Pydantic v2 schemas for SerialNo."""





from __future__ import annotations

from app.stock.serial_no_domain.models.serial_no import (

    SerialNoAssetStatus,

    SerialNoMaintenanceStatus,

    SerialNoStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "SerialNoCreate",

    "SerialNoUpdate",

    "SerialNoRead",

    "SerialNoListResponse",

]





class SerialNoBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    serial_no: str

    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    description: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    asset: Optional[str] = None

    asset_status: Optional[SerialNoAssetStatus] = None

    location: Optional[str] = None

    employee: Optional[str] = None

    maintenance_status: Optional[SerialNoMaintenanceStatus] = None

    warranty_period: Optional[int] = None

    warranty_expiry_date: Optional[dt.date] = None

    amc_expiry_date: Optional[dt.date] = None

    company: str

    work_order: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    purchase_rate: Optional[Decimal] = None

    status: Optional[SerialNoStatus] = None

    customer: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_name: Optional[str] = None

    posting_date: Optional[dt.date] = None





class SerialNoCreate(SerialNoBase):

    pass





class SerialNoUpdate(InputSchema):

    """A partial update."""



    serial_no: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    asset: Optional[str] = None

    asset_status: Optional[SerialNoAssetStatus] = None

    location: Optional[str] = None

    employee: Optional[str] = None

    maintenance_status: Optional[SerialNoMaintenanceStatus] = None

    warranty_period: Optional[int] = None

    warranty_expiry_date: Optional[dt.date] = None

    amc_expiry_date: Optional[dt.date] = None

    company: Optional[str] = None

    work_order: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    purchase_rate: Optional[Decimal] = None

    status: Optional[SerialNoStatus] = None

    customer: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_name: Optional[str] = None

    posting_date: Optional[dt.date] = None





class SerialNoRead(ReadSchema):

    id: uuid.UUID

    name: str

    serial_no: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    item_group_id: Optional[uuid.UUID] = None

    brand_id: Optional[uuid.UUID] = None

    asset: Optional[str] = None

    asset_status: Optional[SerialNoAssetStatus] = None

    location: Optional[str] = None

    employee: Optional[str] = None

    maintenance_status: Optional[SerialNoMaintenanceStatus] = None

    warranty_period: Optional[int] = None

    warranty_expiry_date: Optional[dt.date] = None

    amc_expiry_date: Optional[dt.date] = None

    company: str

    work_order: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None

    batch_no_id: Optional[uuid.UUID] = None

    purchase_rate: Optional[Decimal] = None

    status: Optional[SerialNoStatus] = None

    customer: Optional[str] = None

    reference_doctype: Optional[str] = None

    reference_name: Optional[str] = None

    posting_date: Optional[dt.date] = None





SerialNoListResponse = Page[SerialNoRead]

"""Pydantic v2 schemas for ProductionPlanSalesOrder."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProductionPlanSalesOrderCreate",

    "ProductionPlanSalesOrderRead",

    "ProductionPlanSalesOrderListResponse",

]





class ProductionPlanSalesOrderBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    sales_order_id: uuid.UUID

    sales_order_date: Optional[dt.date] = None

    customer_id: Optional[uuid.UUID] = None

    grand_total: Optional[Decimal] = None

    status: Optional[str] = None





class ProductionPlanSalesOrderCreate(ProductionPlanSalesOrderBase):

    pass





class ProductionPlanSalesOrderUpdate(InputSchema):

    """A partial update."""



    sales_order_id: Optional[uuid.UUID] = None

    sales_order_date: Optional[dt.date] = None

    customer_id: Optional[uuid.UUID] = None

    grand_total: Optional[Decimal] = None

    status: Optional[str] = None





class ProductionPlanSalesOrderRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    sales_order_id: Optional[uuid.UUID] = None

    sales_order_date: Optional[dt.date] = None

    customer_id: Optional[uuid.UUID] = None

    grand_total: Optional[Decimal] = None

    status: Optional[str] = None





ProductionPlanSalesOrderListResponse = Page[ProductionPlanSalesOrderRead]

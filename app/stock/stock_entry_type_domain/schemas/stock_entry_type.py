"""Pydantic v2 schemas for StockEntryType."""





from __future__ import annotations

from app.stock.stock_entry_type_domain.models.stock_entry_type import (

    StockEntryTypePurpose,

)

from typing import Optional

import uuid



from pydantic import Field

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "StockEntryTypeCreate",

    "StockEntryTypeUpdate",

    "StockEntryTypeRead",

    "StockEntryTypeListResponse",

]





class StockEntryTypeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    name: str = Field(min_length=1)

    purpose: StockEntryTypePurpose

    add_to_transit: Optional[bool] = None

    is_standard: Optional[bool] = None





class StockEntryTypeCreate(StockEntryTypeBase):

    pass





class StockEntryTypeUpdate(InputSchema):

    """A partial update."""



    name: Optional[str] = Field(default=None, min_length=1)

    purpose: Optional[StockEntryTypePurpose] = None

    add_to_transit: Optional[bool] = None

    is_standard: Optional[bool] = None





class StockEntryTypeRead(ReadSchema):

    id: uuid.UUID

    name: str

    purpose: Optional[StockEntryTypePurpose] = None

    add_to_transit: Optional[bool] = None

    is_standard: Optional[bool] = None





StockEntryTypeListResponse = Page[StockEntryTypeRead]

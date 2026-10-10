"""Pydantic v2 schemas for ItemBarcode."""





from __future__ import annotations

from app.stock.item_barcode_domain.models.item_barcode import (

    ItemBarcodeBarcodeType,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemBarcodeCreate",

    "ItemBarcodeRead",

    "ItemBarcodeListResponse",

]





class ItemBarcodeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    barcode: str

    barcode_type: Optional[ItemBarcodeBarcodeType] = None

    uom_id: Optional[uuid.UUID] = None





class ItemBarcodeCreate(ItemBarcodeBase):

    pass





class ItemBarcodeUpdate(InputSchema):

    """A partial update."""



    barcode: Optional[str] = None

    barcode_type: Optional[ItemBarcodeBarcodeType] = None

    uom_id: Optional[uuid.UUID] = None





class ItemBarcodeRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    barcode: str

    barcode_type: Optional[ItemBarcodeBarcodeType] = None

    uom_id: Optional[uuid.UUID] = None





ItemBarcodeListResponse = Page[ItemBarcodeRead]

"""Pydantic v2 schemas for PlantFloor."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "PlantFloorCreate",

    "PlantFloorUpdate",

    "PlantFloorRead",

    "PlantFloorListResponse",

]





class PlantFloorBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    floor_name: Optional[str] = None

    company: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None





class PlantFloorCreate(PlantFloorBase):

    pass





class PlantFloorUpdate(InputSchema):

    """A partial update."""



    floor_name: Optional[str] = None

    company: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None





class PlantFloorRead(ReadSchema):

    id: uuid.UUID

    name: str

    floor_name: Optional[str] = None

    company: Optional[str] = None

    warehouse_id: Optional[uuid.UUID] = None





PlantFloorListResponse = Page[PlantFloorRead]

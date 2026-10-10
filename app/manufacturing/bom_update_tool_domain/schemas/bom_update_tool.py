"""Pydantic v2 schemas for BomUpdateTool."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomUpdateToolUpdate",

    "BomUpdateToolRead",

]





class BomUpdateToolUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    current_bom_id: Optional[uuid.UUID] = None

    new_bom_id: Optional[uuid.UUID] = None





class BomUpdateToolRead(ReadSchema):

    id: uuid.UUID

    current_bom_id: Optional[uuid.UUID] = None

    new_bom_id: Optional[uuid.UUID] = None



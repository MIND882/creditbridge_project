"""Pydantic v2 schemas for ChartOfAccountsImporter."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ChartOfAccountsImporterCreate",

    "ChartOfAccountsImporterUpdate",

    "ChartOfAccountsImporterRead",

    "ChartOfAccountsImporterListResponse",

]





class ChartOfAccountsImporterBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    import_file: Optional[str] = None





class ChartOfAccountsImporterCreate(ChartOfAccountsImporterBase):

    pass





class ChartOfAccountsImporterUpdate(InputSchema):

    """A partial update."""



    import_file: Optional[str] = None





class ChartOfAccountsImporterRead(ReadSchema):

    id: uuid.UUID

    name: str

    import_file: Optional[str] = None





ChartOfAccountsImporterListResponse = Page[ChartOfAccountsImporterRead]

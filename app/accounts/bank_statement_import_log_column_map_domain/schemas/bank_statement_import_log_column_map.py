"""Pydantic v2 schemas for BankStatementImportLogColumnMap."""





from __future__ import annotations

from app.accounts.bank_statement_import_log_column_map_domain.models.bank_statement_import_log_column_map import (

    BankStatementImportLogColumnMapMapsTo,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BankStatementImportLogColumnMapCreate",

    "BankStatementImportLogColumnMapRead",

    "BankStatementImportLogColumnMapListResponse",

]





class BankStatementImportLogColumnMapBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    header_text: str

    maps_to: BankStatementImportLogColumnMapMapsTo

    index: Optional[int] = None

    variable: Optional[str] = None





class BankStatementImportLogColumnMapCreate(BankStatementImportLogColumnMapBase):

    """Accepted only nested inside the parent payload."""

    pass





class BankStatementImportLogColumnMapRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    header_text: str

    maps_to: BankStatementImportLogColumnMapMapsTo

    index: int

    variable: Optional[str] = None





BankStatementImportLogColumnMapListResponse = Page[BankStatementImportLogColumnMapRead]

"""Pydantic v2 schemas for BankStatementImport."""





from __future__ import annotations

from app.accounts.bank_statement_import_domain.models.bank_statement_import import (

    BankStatementImportImportType,

    BankStatementImportStatus,

)

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BankStatementImportCreate",

    "BankStatementImportUpdate",

    "BankStatementImportRead",

    "BankStatementImportListResponse",

]





class BankStatementImportBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    bank_account_id: uuid.UUID

    bank_id: Optional[uuid.UUID] = None

    import_file: Optional[str] = None

    template_options: Optional[str] = None

    status: Optional[BankStatementImportStatus] = None

    template_warnings: Optional[str] = None

    show_failed_logs: Optional[bool] = None

    google_sheets_url: Optional[str] = None

    reference_doctype: str

    import_type: BankStatementImportImportType

    submit_after_import: Optional[bool] = None

    mute_emails: Optional[bool] = None

    custom_delimiters: Optional[bool] = None

    delimiter_options: Optional[str] = None

    use_csv_sniffer: Optional[bool] = None

    import_mt940_fromat: Optional[bool] = None





class BankStatementImportCreate(BankStatementImportBase):

    pass





class BankStatementImportUpdate(InputSchema):

    """A partial update."""



    bank_account_id: Optional[uuid.UUID] = None

    bank_id: Optional[uuid.UUID] = None

    import_file: Optional[str] = None

    template_options: Optional[str] = None

    status: Optional[BankStatementImportStatus] = None

    template_warnings: Optional[str] = None

    show_failed_logs: Optional[bool] = None

    google_sheets_url: Optional[str] = None

    reference_doctype: Optional[str] = None

    import_type: Optional[BankStatementImportImportType] = None

    submit_after_import: Optional[bool] = None

    mute_emails: Optional[bool] = None

    custom_delimiters: Optional[bool] = None

    delimiter_options: Optional[str] = None

    use_csv_sniffer: Optional[bool] = None

    import_mt940_fromat: Optional[bool] = None





class BankStatementImportRead(ReadSchema):

    id: uuid.UUID

    name: str

    bank_account_id: uuid.UUID

    bank_id: Optional[uuid.UUID] = None

    import_file: Optional[str] = None

    template_options: Optional[str] = None

    status: Optional[BankStatementImportStatus] = None

    template_warnings: Optional[str] = None

    show_failed_logs: bool

    google_sheets_url: Optional[str] = None

    reference_doctype: str

    import_type: BankStatementImportImportType

    submit_after_import: bool

    mute_emails: bool

    custom_delimiters: bool

    delimiter_options: Optional[str] = None

    use_csv_sniffer: bool

    import_mt940_fromat: bool





BankStatementImportListResponse = Page[BankStatementImportRead]

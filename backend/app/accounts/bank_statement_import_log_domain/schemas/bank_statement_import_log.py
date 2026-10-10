"""Pydantic v2 schemas for BankStatementImportLog."""





from __future__ import annotations

from app.accounts.bank_statement_import_log_domain.models.bank_statement_import_log import (

    BankStatementImportLogDetectedAmountFormat,

    BankStatementImportLogStatus,

)

from decimal import Decimal

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.bank_statement_import_log_column_map_domain.schemas.bank_statement_import_log_column_map import (

    BankStatementImportLogColumnMapCreate,

    BankStatementImportLogColumnMapRead,

)



__all__ = [

    "BankStatementImportLogCreate",

    "BankStatementImportLogUpdate",

    "BankStatementImportLogRead",

    "BankStatementImportLogListResponse",

]





class BankStatementImportLogBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    bank_account_id: uuid.UUID

    number_of_transactions: Optional[int] = None

    closing_balance: Optional[Decimal] = None

    start_date: Optional[dt.date] = None

    end_date: Optional[dt.date] = None

    file: Optional[str] = None

    detected_date_format: Optional[str] = None

    detected_amount_format: Optional[BankStatementImportLogDetectedAmountFormat] = None

    detected_header_index: Optional[int] = None

    detected_transaction_starting_index: Optional[int] = None

    detected_transaction_ending_index: Optional[int] = None

    pdf_tables: Optional[str] = None

    status: Optional[BankStatementImportLogStatus] = None

    currency: Optional[str] = None

    total_debits: Optional[Decimal] = None

    total_credits: Optional[Decimal] = None

    total_debit_transactions: Optional[int] = None

    total_credit_transactions: Optional[int] = None



    column_mapping: list[BankStatementImportLogColumnMapCreate] = []





class BankStatementImportLogCreate(BankStatementImportLogBase):

    pass





class BankStatementImportLogUpdate(InputSchema):

    """A partial update."""



    bank_account_id: Optional[uuid.UUID] = None

    number_of_transactions: Optional[int] = None

    closing_balance: Optional[Decimal] = None

    start_date: Optional[dt.date] = None

    end_date: Optional[dt.date] = None

    file: Optional[str] = None

    detected_date_format: Optional[str] = None

    detected_amount_format: Optional[BankStatementImportLogDetectedAmountFormat] = None

    detected_header_index: Optional[int] = None

    detected_transaction_starting_index: Optional[int] = None

    detected_transaction_ending_index: Optional[int] = None

    pdf_tables: Optional[str] = None

    status: Optional[BankStatementImportLogStatus] = None

    currency: Optional[str] = None

    total_debits: Optional[Decimal] = None

    total_credits: Optional[Decimal] = None

    total_debit_transactions: Optional[int] = None

    total_credit_transactions: Optional[int] = None

    column_mapping: Optional[list[BankStatementImportLogColumnMapCreate]] = None





class BankStatementImportLogRead(ReadSchema):

    id: uuid.UUID

    name: str

    bank_account_id: uuid.UUID

    number_of_transactions: Optional[int] = None

    closing_balance: Optional[Decimal] = None

    start_date: Optional[dt.date] = None

    end_date: Optional[dt.date] = None

    file: Optional[str] = None

    detected_date_format: Optional[str] = None

    detected_amount_format: Optional[BankStatementImportLogDetectedAmountFormat] = None

    detected_header_index: Optional[int] = None

    detected_transaction_starting_index: Optional[int] = None

    detected_transaction_ending_index: Optional[int] = None

    pdf_tables: Optional[str] = None

    status: Optional[BankStatementImportLogStatus] = None

    currency: Optional[str] = None

    total_debits: Optional[Decimal] = None

    total_credits: Optional[Decimal] = None

    total_debit_transactions: Optional[int] = None

    total_credit_transactions: Optional[int] = None

    column_mapping: list[BankStatementImportLogColumnMapRead] = []





BankStatementImportLogListResponse = Page[BankStatementImportLogRead]

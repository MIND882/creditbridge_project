"""Pydantic v2 schemas for ProcessStatementOfAccounts."""





from __future__ import annotations

from app.accounts.process_statement_of_accounts_domain.models.process_statement_of_accounts import (

    ProcessStatementOfAccountsAgeingBasedOn,

    ProcessStatementOfAccountsCategorizeBy,

    ProcessStatementOfAccountsCustomerCollection,

    ProcessStatementOfAccountsFrequency,

    ProcessStatementOfAccountsOrientation,

    ProcessStatementOfAccountsReport,

)

from typing import Optional

import datetime as dt

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



from app.accounts.psoa_cost_center_domain.schemas.psoa_cost_center import (

    PsoaCostCenterCreate,

    PsoaCostCenterRead,

)

from app.accounts.psoa_project_domain.schemas.psoa_project import (

    PsoaProjectCreate,

    PsoaProjectRead,

)

from app.accounts.process_statement_of_accounts_cc_domain.schemas.process_statement_of_accounts_cc import (

    ProcessStatementOfAccountsCcCreate,

    ProcessStatementOfAccountsCcRead,

)

from app.accounts.process_statement_of_accounts_customer_domain.schemas.process_statement_of_accounts_customer import (

    ProcessStatementOfAccountsCustomerCreate,

    ProcessStatementOfAccountsCustomerRead,

)



__all__ = [

    "ProcessStatementOfAccountsCreate",

    "ProcessStatementOfAccountsUpdate",

    "ProcessStatementOfAccountsRead",

    "ProcessStatementOfAccountsListResponse",

]





class ProcessStatementOfAccountsBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    frequency: Optional[ProcessStatementOfAccountsFrequency] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    customer_collection: Optional[ProcessStatementOfAccountsCustomerCollection] = None

    collection_name: Optional[str] = None

    account_id: Optional[uuid.UUID] = None

    finance_book_id: Optional[uuid.UUID] = None

    orientation: Optional[ProcessStatementOfAccountsOrientation] = None

    start_date: Optional[dt.date] = None

    currency: Optional[str] = None

    include_ageing: Optional[bool] = None

    ageing_based_on: Optional[ProcessStatementOfAccountsAgeingBasedOn] = None

    enable_auto_email: Optional[bool] = None

    primary_mandatory: Optional[bool] = None

    filter_duration: Optional[int] = None

    subject: Optional[str] = None

    body: Optional[str] = None

    letter_head: Optional[str] = None

    terms_and_conditions: Optional[str] = None

    include_break: Optional[bool] = None

    show_net_values_in_party_account: Optional[bool] = None

    sender: Optional[str] = None

    report: ProcessStatementOfAccountsReport

    posting_date: Optional[dt.date] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    sales_partner: Optional[str] = None

    sales_person: Optional[str] = None

    territory: Optional[str] = None

    based_on_payment_terms: Optional[bool] = None

    pdf_name: Optional[str] = None

    ignore_exchange_rate_revaluation_journals: Optional[bool] = None

    ignore_cr_dr_notes: Optional[bool] = None

    show_remarks: Optional[bool] = None

    categorize_by: Optional[ProcessStatementOfAccountsCategorizeBy] = None

    show_future_payments: Optional[bool] = None

    print_format: Optional[str] = None

    show_opening_entries: Optional[bool] = None



    cost_center: list[PsoaCostCenterCreate] = []



    project: list[PsoaProjectCreate] = []



    cc_to: list[ProcessStatementOfAccountsCcCreate] = []



    customers: list[ProcessStatementOfAccountsCustomerCreate] = []





class ProcessStatementOfAccountsCreate(ProcessStatementOfAccountsBase):

    pass





class ProcessStatementOfAccountsUpdate(InputSchema):

    """A partial update."""



    frequency: Optional[ProcessStatementOfAccountsFrequency] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    customer_collection: Optional[ProcessStatementOfAccountsCustomerCollection] = None

    collection_name: Optional[str] = None

    account_id: Optional[uuid.UUID] = None

    finance_book_id: Optional[uuid.UUID] = None

    orientation: Optional[ProcessStatementOfAccountsOrientation] = None

    start_date: Optional[dt.date] = None

    currency: Optional[str] = None

    include_ageing: Optional[bool] = None

    ageing_based_on: Optional[ProcessStatementOfAccountsAgeingBasedOn] = None

    enable_auto_email: Optional[bool] = None

    primary_mandatory: Optional[bool] = None

    filter_duration: Optional[int] = None

    subject: Optional[str] = None

    body: Optional[str] = None

    letter_head: Optional[str] = None

    terms_and_conditions: Optional[str] = None

    include_break: Optional[bool] = None

    show_net_values_in_party_account: Optional[bool] = None

    sender: Optional[str] = None

    report: Optional[ProcessStatementOfAccountsReport] = None

    posting_date: Optional[dt.date] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    sales_partner: Optional[str] = None

    sales_person: Optional[str] = None

    territory: Optional[str] = None

    based_on_payment_terms: Optional[bool] = None

    pdf_name: Optional[str] = None

    ignore_exchange_rate_revaluation_journals: Optional[bool] = None

    ignore_cr_dr_notes: Optional[bool] = None

    show_remarks: Optional[bool] = None

    categorize_by: Optional[ProcessStatementOfAccountsCategorizeBy] = None

    show_future_payments: Optional[bool] = None

    print_format: Optional[str] = None

    show_opening_entries: Optional[bool] = None

    cost_center: Optional[list[PsoaCostCenterCreate]] = None

    project: Optional[list[PsoaProjectCreate]] = None

    cc_to: Optional[list[ProcessStatementOfAccountsCcCreate]] = None

    customers: Optional[list[ProcessStatementOfAccountsCustomerCreate]] = None





class ProcessStatementOfAccountsRead(ReadSchema):

    id: uuid.UUID

    name: str

    frequency: Optional[ProcessStatementOfAccountsFrequency] = None

    from_date: Optional[dt.date] = None

    to_date: Optional[dt.date] = None

    customer_collection: Optional[ProcessStatementOfAccountsCustomerCollection] = None

    collection_name: Optional[str] = None

    account_id: Optional[uuid.UUID] = None

    finance_book_id: Optional[uuid.UUID] = None

    orientation: Optional[ProcessStatementOfAccountsOrientation] = None

    start_date: Optional[dt.date] = None

    currency: Optional[str] = None

    include_ageing: bool

    ageing_based_on: Optional[ProcessStatementOfAccountsAgeingBasedOn] = None

    enable_auto_email: bool

    primary_mandatory: bool

    filter_duration: Optional[int] = None

    subject: Optional[str] = None

    body: Optional[str] = None

    letter_head: Optional[str] = None

    terms_and_conditions: Optional[str] = None

    include_break: bool

    show_net_values_in_party_account: bool

    sender: Optional[str] = None

    report: ProcessStatementOfAccountsReport

    posting_date: Optional[dt.date] = None

    payment_terms_template_id: Optional[uuid.UUID] = None

    sales_partner: Optional[str] = None

    sales_person: Optional[str] = None

    territory: Optional[str] = None

    based_on_payment_terms: bool

    pdf_name: Optional[str] = None

    ignore_exchange_rate_revaluation_journals: bool

    ignore_cr_dr_notes: bool

    show_remarks: bool

    categorize_by: Optional[ProcessStatementOfAccountsCategorizeBy] = None

    show_future_payments: bool

    print_format: Optional[str] = None

    show_opening_entries: bool

    cost_center: list[PsoaCostCenterRead] = []

    project: list[PsoaProjectRead] = []

    cc_to: list[ProcessStatementOfAccountsCcRead] = []

    customers: list[ProcessStatementOfAccountsCustomerRead] = []





ProcessStatementOfAccountsListResponse = Page[ProcessStatementOfAccountsRead]

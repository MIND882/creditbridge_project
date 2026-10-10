"""

Process Statement Of Accounts -- converted from ``erpnext/accounts/doctype/process_statement_of_accounts``.





"""



from __future__ import annotations



import datetime as dt

import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Date, Enum as SAEnum, ForeignKey, Integer, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.process_statement_of_accounts_cc_domain.models.process_statement_of_accounts_cc import ProcessStatementOfAccountsCc

from app.accounts.process_statement_of_accounts_customer_domain.models.process_statement_of_accounts_customer import ProcessStatementOfAccountsCustomer

from app.accounts.psoa_cost_center_domain.models.psoa_cost_center import PsoaCostCenter

from app.accounts.psoa_project_domain.models.psoa_project import PsoaProject



from app.accounts.account_domain.models.account import Account  # noqa: F401

from app.accounts.finance_book_domain.models.finance_book import FinanceBook  # noqa: F401

from app.accounts.payment_terms_template_domain.models.payment_terms_template import PaymentTermsTemplate  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["ProcessStatementOfAccounts", "ProcessStatementOfAccountsFrequency", "ProcessStatementOfAccountsCustomerCollection", "ProcessStatementOfAccountsOrientation", "ProcessStatementOfAccountsAgeingBasedOn", "ProcessStatementOfAccountsReport", "ProcessStatementOfAccountsCategorizeBy"]







class ProcessStatementOfAccountsFrequency(str, enum.Enum):

    DAILY = "Daily"

    WEEKLY = "Weekly"

    BIWEEKLY = "Biweekly"

    MONTHLY = "Monthly"

    QUARTERLY = "Quarterly"





class ProcessStatementOfAccountsCustomerCollection(str, enum.Enum):

    CUSTOMER_GROUP = "Customer Group"

    TERRITORY = "Territory"

    SALES_PARTNER = "Sales Partner"

    SALES_PERSON = "Sales Person"





class ProcessStatementOfAccountsOrientation(str, enum.Enum):

    LANDSCAPE = "Landscape"

    PORTRAIT = "Portrait"





class ProcessStatementOfAccountsAgeingBasedOn(str, enum.Enum):

    DUE_DATE = "Due Date"

    POSTING_DATE = "Posting Date"





class ProcessStatementOfAccountsReport(str, enum.Enum):

    GENERAL_LEDGER = "General Ledger"

    ACCOUNTS_RECEIVABLE = "Accounts Receivable"





class ProcessStatementOfAccountsCategorizeBy(str, enum.Enum):

    CATEGORIZE_BY_VOUCHER = "Categorize by Voucher"

    CATEGORIZE_BY_VOUCHER_CONSOLIDATED = "Categorize by Voucher (Consolidated)"









class ProcessStatementOfAccounts(TenantModel):

    __tablename__ = "process_statement_of_accounts"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_process_statement_of_accounts_business_name"),

    )



    #: ``autoname`` = 'Prompt'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    frequency: Mapped[Optional[ProcessStatementOfAccountsFrequency]] = mapped_column(

        SAEnum(ProcessStatementOfAccountsFrequency, native_enum=False, length=9, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    from_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    to_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    customer_collection: Mapped[Optional[ProcessStatementOfAccountsCustomerCollection]] = mapped_column(

        SAEnum(ProcessStatementOfAccountsCustomerCollection, native_enum=False, length=14, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    collection_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    finance_book_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("finance_books.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    finance_book = relationship("FinanceBook", foreign_keys=[finance_book_id])

    orientation: Mapped[Optional[ProcessStatementOfAccountsOrientation]] = mapped_column(

        SAEnum(ProcessStatementOfAccountsOrientation, native_enum=False, length=9, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    start_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    include_ageing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    ageing_based_on: Mapped[Optional[ProcessStatementOfAccountsAgeingBasedOn]] = mapped_column(

        SAEnum(ProcessStatementOfAccountsAgeingBasedOn, native_enum=False, length=12, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    enable_auto_email: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    primary_mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    filter_duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    subject: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    letter_head: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    terms_and_conditions: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    include_break: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    show_net_values_in_party_account: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    sender: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    report: Mapped[ProcessStatementOfAccountsReport] = mapped_column(

        SAEnum(ProcessStatementOfAccountsReport, native_enum=False, length=19, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    posting_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    payment_terms_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("payment_terms_templates.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    payment_terms_template = relationship("PaymentTermsTemplate", foreign_keys=[payment_terms_template_id])

    sales_partner: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    sales_person: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    territory: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    based_on_payment_terms: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    pdf_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    ignore_exchange_rate_revaluation_journals: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    ignore_cr_dr_notes: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    show_remarks: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    categorize_by: Mapped[Optional[ProcessStatementOfAccountsCategorizeBy]] = mapped_column(

        SAEnum(ProcessStatementOfAccountsCategorizeBy, native_enum=False, length=36, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    show_future_payments: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    print_format: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    show_opening_entries: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    cost_center = relationship(

        PsoaCostCenter,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PsoaCostCenter.idx,

        passive_deletes=True,

    )

    project = relationship(

        PsoaProject,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=PsoaProject.idx,

        passive_deletes=True,

    )

    cc_to = relationship(

        ProcessStatementOfAccountsCc,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=ProcessStatementOfAccountsCc.idx,

        passive_deletes=True,

    )

    customers = relationship(

        ProcessStatementOfAccountsCustomer,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=ProcessStatementOfAccountsCustomer.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ProcessStatementOfAccounts id={self.id}>"

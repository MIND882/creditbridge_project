"""

Bank Statement Import Log -- converted from ``erpnext/accounts/doctype/bank_statement_import_log``.





"""



from __future__ import annotations



import datetime as dt

import enum

from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.bank_statement_import_log_column_map_domain.models.bank_statement_import_log_column_map import BankStatementImportLogColumnMap



from app.accounts.bank_account_domain.models.bank_account import BankAccount  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["BankStatementImportLog", "BankStatementImportLogDetectedAmountFormat", "BankStatementImportLogStatus"]







class BankStatementImportLogDetectedAmountFormat(str, enum.Enum):

    SEPARATE_COLUMNS_FOR_WITHDRAWAL_AND_DEPOSIT = "Separate columns for withdrawal and deposit"

    AMOUNT_COLUMN_HAS_CR_DR_VALUES = "Amount column has \"CR\"/\"DR\" values"

    AMOUNT_COLUMN_HAS_POSITIVE_NEGATIVE_VALUES = "Amount column has positive/negative values"

    TRANSACTION_TYPE_COLUMN_HAS_CR_DR_VALUES = "Transaction type column has \"CR\"/\"DR\" values"

    TRANSACTION_TYPE_COLUMN_HAS_DEPOSIT_WITHDRAWAL_VALUES = "Transaction type column has \"Deposit\"/\"Withdrawal\" values"

    TRANSACTION_TYPE_COLUMN_HAS_C_D_VALUES = "Transaction type column has \"C\"/\"D\" values"





class BankStatementImportLogStatus(str, enum.Enum):

    NOT_STARTED = "Not Started"

    COMPLETED = "Completed"









class BankStatementImportLog(TenantModel):

    __tablename__ = "bank_statement_import_logs"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bank_statement_import_logs_business_name"),

    )



    #: ``autoname`` = 'hash'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])

    number_of_transactions: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    closing_balance: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    start_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    end_date: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)

    file: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    detected_date_format: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    detected_amount_format: Mapped[Optional[BankStatementImportLogDetectedAmountFormat]] = mapped_column(

        SAEnum(BankStatementImportLogDetectedAmountFormat, native_enum=False, length=57, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    detected_header_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    detected_transaction_starting_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    detected_transaction_ending_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    pdf_tables: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[Optional[BankStatementImportLogStatus]] = mapped_column(

        SAEnum(BankStatementImportLogStatus, native_enum=False, length=11, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=True,

    )

    currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    total_debits: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_credits: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    total_debit_transactions: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    total_credit_transactions: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



    column_mapping = relationship(

        BankStatementImportLogColumnMap,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=BankStatementImportLogColumnMap.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankStatementImportLog id={self.id}>"

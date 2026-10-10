"""

Bank Statement Import Log Column Map -- converted from ``erpnext/accounts/doctype/bank_statement_import_log_column_map``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["BankStatementImportLogColumnMap", "BankStatementImportLogColumnMapMapsTo"]







class BankStatementImportLogColumnMapMapsTo(str, enum.Enum):

    DO_NOT_IMPORT = "Do not import"

    DATE = "Date"

    WITHDRAWAL = "Withdrawal"

    DEPOSIT = "Deposit"

    AMOUNT = "Amount"

    DESCRIPTION = "Description"

    REFERENCE = "Reference"

    TRANSACTION_TYPE = "Transaction Type"

    DEBIT_CREDIT = "Debit/Credit"

    BALANCE = "Balance"

    INCLUDED_FEE = "Included Fee"

    EXCLUDED_FEE = "Excluded Fee"

    PARTY_NAME_ACCOUNT_HOLDER = "Party Name/Account Holder"

    PARTY_ACCOUNT_NO = "Party Account No."

    PARTY_IBAN = "Party IBAN"









class BankStatementImportLogColumnMap(ChildTableModel, TenantModel):

    __tablename__ = "bank_statement_import_log_column_maps"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("bank_statement_import_logs.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("BankStatementImportLog", back_populates="column_mapping", foreign_keys=[parent_id])



    header_text: Mapped[str] = mapped_column(String(140), nullable=False)

    maps_to: Mapped[BankStatementImportLogColumnMapMapsTo] = mapped_column(

        SAEnum(BankStatementImportLogColumnMapMapsTo, native_enum=False, length=25, validate_strings=True, values_callable=lambda e: [m.value for m in e]),

        nullable=False,

    )

    index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    variable: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankStatementImportLogColumnMap id={self.id}>"

"""

Bank Statement Import -- converted from ``erpnext/accounts/doctype/bank_statement_import``.





"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, String, Text, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.bank_account_domain.models.bank_account import BankAccount  # noqa: F401

from app.accounts.bank_domain.models.bank import Bank  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["BankStatementImport", "BankStatementImportStatus", "BankStatementImportImportType"]







class BankStatementImportStatus(str, enum.Enum):

    PENDING = "Pending"

    SUCCESS = "Success"

    PARTIAL_SUCCESS = "Partial Success"

    ERROR = "Error"





class BankStatementImportImportType(str, enum.Enum):

    INSERT_NEW_RECORDS = "Insert New Records"

    UPDATE_EXISTING_RECORDS = "Update Existing Records"









class BankStatementImport(TenantModel):

    __tablename__ = "bank_statement_imports"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_bank_statement_imports_business_name"),

    )



    #: ``autoname`` = 'format:Bank Statement Import on {creation}'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])

    bank_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("banks.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    bank = relationship("Bank", foreign_keys=[bank_id])

    import_file: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    template_options: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[Optional[BankStatementImportStatus]] = mapped_column(

        SAEnum(BankStatementImportStatus, native_enum=False, length=15, validate_strings=True),

        nullable=True,

    )

    template_warnings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    show_failed_logs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    google_sheets_url: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_doctype: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)

    import_type: Mapped[BankStatementImportImportType] = mapped_column(

        SAEnum(BankStatementImportImportType, native_enum=False, length=23, validate_strings=True),

        nullable=False,

    )

    submit_after_import: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    mute_emails: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    custom_delimiters: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    delimiter_options: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    use_csv_sniffer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    import_mt940_fromat: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<BankStatementImport id={self.id}>"

"""

JournalEntryAccount -- converted from ``erpnext/accounts/doctype/journal_entry_account``.



Rows only ever exist inside a parent, so the API is read-only.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import Date, Float, ForeignKey, Numeric, String, Text, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["JournalEntryAccount"]





class JournalEntryAccount(ChildTableModel, TenantModel):

    """One row of ``JournalEntry.accounts``."""



    __tablename__ = "journal_entry_accounts"



    parent_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("journal_entries.id", ondelete="CASCADE"), nullable=False, index=True

    )

    parent = relationship("JournalEntry", back_populates="accounts", foreign_keys=[parent_id])



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])

    account_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    cost_center_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("cost_centers.id", ondelete="RESTRICT"),

        nullable=True, index=True

    )

    cost_center = relationship("CostCenter", foreign_keys=[cost_center_id])

    party_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    party: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    account_currency: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    exchange_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    debit_in_account_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    debit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    credit_in_account_currency: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    credit: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    reference_type: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    project: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    is_advance: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    user_remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    against_account: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    bank_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("acc_bank_accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True

    )

    bank_account = relationship("app.accounts.bank_account_domain.models.bank_account.BankAccount", foreign_keys=[bank_account_id])

    reference_detail_no: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<JournalEntryAccount id={self.id}>"

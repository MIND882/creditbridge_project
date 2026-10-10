"""

Ledger Merge -- converted from ``erpnext/accounts/doctype/ledger_merge``.





"""



from __future__ import annotations



import enum

from typing import Optional

import uuid



from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.ledger_merge_accounts_domain.models.ledger_merge_accounts import LedgerMergeAccounts



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel



__all__ = ["LedgerMerge", "LedgerMergeStatus", "LedgerMergeRootType"]







class LedgerMergeStatus(str, enum.Enum):

    PENDING = "Pending"

    SUCCESS = "Success"

    PARTIAL_SUCCESS = "Partial Success"

    ERROR = "Error"





class LedgerMergeRootType(str, enum.Enum):

    ASSET = "Asset"

    LIABILITY = "Liability"

    INCOME = "Income"

    EXPENSE = "Expense"

    EQUITY = "Equity"









class LedgerMerge(TenantModel):

    __tablename__ = "ledger_merges"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_ledger_merges_business_name"),

    )



    #: ``autoname`` = 'format:{account_name} merger on {creation}'.

    name: Mapped[str] = mapped_column(String(140), nullable=False)



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    status: Mapped[Optional[LedgerMergeStatus]] = mapped_column(

        SAEnum(LedgerMergeStatus, native_enum=False, length=15, validate_strings=True),

        nullable=True,

    )

    root_type: Mapped[LedgerMergeRootType] = mapped_column(

        SAEnum(LedgerMergeRootType, native_enum=False, length=9, validate_strings=True),

        nullable=False,

    )

    account_name: Mapped[str] = mapped_column(String(140), nullable=False)

    is_group: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)



    merge_accounts = relationship(

        LedgerMergeAccounts,

        back_populates="parent",

        cascade="all, delete-orphan",

        order_by=LedgerMergeAccounts.idx,

        passive_deletes=True,

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LedgerMerge id={self.id}>"

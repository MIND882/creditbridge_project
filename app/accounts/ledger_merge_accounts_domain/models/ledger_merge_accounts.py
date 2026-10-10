"""

Ledger Merge Accounts -- converted from ``erpnext/accounts/doctype/ledger_merge_accounts``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Boolean, ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["LedgerMergeAccounts"]







class LedgerMergeAccounts(ChildTableModel, TenantModel):

    __tablename__ = "ledger_merge_accounts"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("ledger_merges.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("LedgerMerge", back_populates="merge_accounts", foreign_keys=[parent_id])



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=False, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])

    merged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    account_name: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LedgerMergeAccounts id={self.id}>"

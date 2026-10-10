"""

POS Closing Entry Taxes -- converted from ``erpnext/accounts/doctype/pos_closing_entry_taxes``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["POSClosingEntryTaxes"]







class POSClosingEntryTaxes(ChildTableModel, TenantModel):

    __tablename__ = "pos_closing_entry_taxes"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("pos_closing_entries.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("POSClosingEntry", back_populates="taxes", foreign_keys=[parent_id])



    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    account_head_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account_head = relationship("Account", foreign_keys=[account_head_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<POSClosingEntryTaxes id={self.id}>"

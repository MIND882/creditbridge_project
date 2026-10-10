"""

PartyAccount -- converted from ``erpnext/accounts/doctype/party_account``.



Customer/Supplier are not converted yet, so this stands alone

keyed on a party label rather than hanging off a parent.

"""



from __future__ import annotations



import uuid

from datetime import date

from decimal import Decimal

from typing import Optional



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PartyAccount"]





class PartyAccount(TenantModel):

    """One row of ``PartyAccount.rows``."""



    __tablename__ = "party_accounts"



    party_account_of: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True

    )

    account = relationship("Account", foreign_keys=[account_id])

    advance_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True

    )

    advance_account = relationship("Account", foreign_keys=[advance_account_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PartyAccount id={self.id}>"

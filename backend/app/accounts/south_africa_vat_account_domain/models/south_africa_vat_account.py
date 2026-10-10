"""

South Africa Vat Account -- converted from ``erpnext/accounts/doctype/south_africa_vat_account``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.accounts.account_domain.models.account import Account  # noqa: F401



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SouthAfricaVatAccount"]







class SouthAfricaVatAccount(ChildTableModel, TenantModel):

    __tablename__ = "south_africa_vat_accounts"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_south_africa_vat_accounts_business_name"),

    )



    #: ``autoname`` = 'account'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"),

        nullable=True, index=True,

    )

    account = relationship("Account", foreign_keys=[account_id])



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SouthAfricaVatAccount id={self.id}>"

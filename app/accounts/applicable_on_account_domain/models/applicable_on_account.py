"""

Applicable On Account -- converted from ``erpnext/accounts/doctype/applicable_on_account``.



A Frappe child table (``istable: 1``): no independent identity, owned by a

Accounting Dimension Filter, ordered by ``idx``, never addressed by its own write API.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import Boolean, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ApplicableOnAccount"]





class ApplicableOnAccount(ChildTableModel, TenantModel):

    """One row of a Accounting Dimension Filter."""



    __tablename__ = "applicable_on_accounts"



    #: Re-declared from the mixin with a concrete FK so the constraint is real.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounting_dimension_filters.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship("AccountingDimensionFilter", back_populates="accounts")



    account_id: Mapped[uuid.UUID] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False

    )

    is_mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ApplicableOnAccount id={self.id}>"

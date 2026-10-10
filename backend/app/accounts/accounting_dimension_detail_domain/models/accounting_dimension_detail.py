"""

Accounting Dimension Detail -- converted from ``erpnext/accounts/doctype/accounting_dimension_detail``.



A Frappe child table (``istable: 1``): no independent identity, owned by a

Accounting Dimension, ordered by ``idx``, never addressed by its own write API.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import Boolean, ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["AccountingDimensionDetail"]





class AccountingDimensionDetail(ChildTableModel, TenantModel):

    """One row of a Accounting Dimension."""



    __tablename__ = "accounting_dimension_details"



    #: Re-declared from the mixin with a concrete FK so the constraint is real.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounting_dimensions.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship("AccountingDimension", back_populates="dimension_defaults")



    company: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    reference_document: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    default_dimension: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    mandatory_for_bs: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    mandatory_for_pl: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    automatically_post_balancing_accounting_entry: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    offsetting_account_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=True

    )



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AccountingDimensionDetail id={self.id}>"

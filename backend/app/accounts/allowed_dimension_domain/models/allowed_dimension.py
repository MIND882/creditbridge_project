"""

Allowed Dimension -- converted from ``erpnext/accounts/doctype/allowed_dimension``.



A Frappe child table (``istable: 1``): no independent identity, owned by a

Accounting Dimension Filter, ordered by ``idx``, never addressed by its own write API.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["AllowedDimension"]





class AllowedDimension(ChildTableModel, TenantModel):

    """One row of a Accounting Dimension Filter."""



    __tablename__ = "allowed_dimensions"



    #: Re-declared from the mixin with a concrete FK so the constraint is real.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("accounting_dimension_filters.id", ondelete="CASCADE"), nullable=True, index=True

    )

    parent = relationship("AccountingDimensionFilter", back_populates="dimensions")



    accounting_dimension: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    dimension_value: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<AllowedDimension id={self.id}>"

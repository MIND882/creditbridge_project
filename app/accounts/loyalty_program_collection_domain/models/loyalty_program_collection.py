"""

Loyalty Program Collection -- converted from ``erpnext/accounts/doctype/loyalty_program_collection``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from decimal import Decimal

from typing import Optional

import uuid



from sqlalchemy import ForeignKey, Numeric, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["LoyaltyProgramCollection"]







class LoyaltyProgramCollection(ChildTableModel, TenantModel):

    __tablename__ = "loyalty_program_collections"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("loyalty_programs.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("LoyaltyProgram", back_populates="collection_rules", foreign_keys=[parent_id])



    tier_name: Mapped[str] = mapped_column(String(140), nullable=False)

    min_spent: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    collection_factor: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<LoyaltyProgramCollection id={self.id}>"

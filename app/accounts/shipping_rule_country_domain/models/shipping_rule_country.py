"""

Shipping Rule Country -- converted from ``erpnext/accounts/doctype/shipping_rule_country``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ShippingRuleCountry"]







class ShippingRuleCountry(ChildTableModel, TenantModel):

    __tablename__ = "shipping_rule_countries"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipping_rules.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("ShippingRule", back_populates="countries", foreign_keys=[parent_id])



    country: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ShippingRuleCountry id={self.id}>"

"""

Shipping Rule Condition -- converted from ``erpnext/accounts/doctype/shipping_rule_condition``.



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



__all__ = ["ShippingRuleCondition"]







class ShippingRuleCondition(ChildTableModel, TenantModel):

    __tablename__ = "shipping_rule_conditions"

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("shipping_rules.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship("ShippingRule", back_populates="conditions", foreign_keys=[parent_id])



    from_value: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)

    to_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(21, 9), nullable=True)

    shipping_amount: Mapped[Decimal] = mapped_column(Numeric(21, 9), nullable=False, default=0)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ShippingRuleCondition id={self.id}>"

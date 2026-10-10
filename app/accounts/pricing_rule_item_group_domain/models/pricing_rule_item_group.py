"""

Pricing Rule Item Group -- converted from ``erpnext/accounts/doctype/pricing_rule_item_group``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import String, Uuid

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["PricingRuleItemGroup"]







class PricingRuleItemGroup(ChildTableModel, TenantModel):

    __tablename__ = "pricing_rule_item_groups"

    #: Polymorphic parent -- pricing_rule, promotional_scheme

    #: all use this doctype as a Table, so there is no single

    #: foreign key to point at. ``parenttype`` says which.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        Uuid, nullable=True, index=True

    )

    parenttype: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True, index=True

    )



    item_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    uom: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<PricingRuleItemGroup id={self.id}>"

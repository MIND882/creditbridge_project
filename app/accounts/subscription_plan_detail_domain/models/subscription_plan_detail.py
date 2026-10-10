"""

Subscription Plan Detail -- converted from ``erpnext/accounts/doctype/subscription_plan_detail``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent.

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import Integer, String, Uuid

from sqlalchemy.orm import Mapped, mapped_column



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["SubscriptionPlanDetail"]







class SubscriptionPlanDetail(ChildTableModel, TenantModel):

    __tablename__ = "subscription_plan_details"

    #: Polymorphic parent -- payment_request, subscription

    #: all use this doctype as a Table, so there is no single

    #: foreign key to point at. ``parenttype`` says which.

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        Uuid, nullable=True, index=True

    )

    parenttype: Mapped[Optional[str]] = mapped_column(

        String(140), nullable=True, index=True

    )



    qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    plan: Mapped[Optional[str]] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<SubscriptionPlanDetail id={self.id}>"

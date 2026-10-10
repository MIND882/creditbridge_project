"""

Item Customer Detail -- converted from ``erpnext/stock/doctype/item_customer_detail``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Item).

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ItemCustomerDetail"]







class ItemCustomerDetail(ChildTableModel, TenantModel):

    __tablename__ = "item_customer_details"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_customer_details_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("items.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "Item",

        back_populates="customer_items",

        # explicit: a child can carry a second FK to its own parent

        # (item_variant_attribute.variant_of -> items), which would

        # otherwise make the join ambiguous

        foreign_keys=[parent_id],

    )



    #: ``autoname`` = 'hash'.

    #: Upstream ``autoname = 'hash'``: Frappe assigns an opaque random hash.

    #: There is no content to hash here, so a UUID4 is the faithful

    #: equivalent -- unique, opaque, and not user-visible. Without a

    #: default the column is NOT NULL and every insert fails.

    name: Mapped[str] = mapped_column(

        String(140), nullable=False, default=lambda: uuid.uuid4().hex

    )



    customer_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    customer_group: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)

    ref_code: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemCustomerDetail id={self.id}>"

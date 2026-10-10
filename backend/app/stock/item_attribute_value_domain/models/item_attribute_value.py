"""

Item Attribute Value -- converted from ``erpnext/stock/doctype/item_attribute_value``.



A Frappe child table (``istable: 1``): no independent identity, owned by its parent (Item Attribute).

"""



from __future__ import annotations



from typing import Optional

import uuid



from sqlalchemy import ForeignKey, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.core.base_model import TenantModel

from app.core.docstatus import ChildTableModel



__all__ = ["ItemAttributeValue"]







class ItemAttributeValue(ChildTableModel, TenantModel):

    __tablename__ = "item_attribute_values"

    __table_args__ = (

        UniqueConstraint("business_id", "name", name="uq_item_attribute_values_business_name"),

    )



    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(

        ForeignKey("item_attributes.id", ondelete="CASCADE"),

        nullable=True, index=True,

    )

    parent = relationship(  # noqa: F821 - resolved by the parent module

        "ItemAttribute",

        back_populates="item_attribute_values",

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



    attribute_value: Mapped[str] = mapped_column(String(140), nullable=False)

    abbr: Mapped[str] = mapped_column(String(140), nullable=False)



    def __repr__(self) -> str:  # pragma: no cover - debugging aid

        return f"<ItemAttributeValue id={self.id}>"
